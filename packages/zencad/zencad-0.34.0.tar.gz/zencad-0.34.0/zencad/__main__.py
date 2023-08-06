#!/usr/bin/env python3
# coding:utf-8

import os
import sys
import time
import zencad
import zencad.version
import zencad.showapi
import zencad.gui.application
import zencad.gui.viewadaptor
import zencad.gui.retransler
import zencad.lazifier
import zencad.gui.mainwindow
import runpy

import pickle
import sys, traceback
import argparse
import subprocess
import threading
import multiprocessing
import base64
import psutil
import signal

from zencad.util import print_to_stderr

import zencad.configure

def trace(*args):
	if zencad.configure.CONFIGURE_MAIN_TRACE: 
		sys.stderr.write(str(args))
		sys.stderr.write("\r\n")
		sys.stderr.flush()

def finish_procedure():
	trace("MAIN FINISH")

	trace("MAIN: Wait childs ...")
	trace("MAIN:  list of threads: ", threading.enumerate())

	if zencad.gui.application.CONSOLE_RETRANS_THREAD:
		zencad.gui.application.CONSOLE_RETRANS_THREAD.finish()
	
	def on_terminate(proc):
		trace("process {} finished with exit code {}".format(proc, proc.returncode))
	
	procs = psutil.Process().children()
	psutil.wait_procs(procs, callback=on_terminate)
	#for p in procs:
	#    p.terminate()
	#gone, alive = psutil.wait_procs(procs, timeout=3, callback=on_terminate)
	#for p in alive:
	#    p.kill()
	trace("MAIN: Wait childs ... OK")

def protect_path(s):
	if s[0]==s[-1] and (s[0] == "'" or s[0] == '"'):
		return s[1:-1]
	return s

def do_main():
	#os.closerange(3, 100)

	OPPOSITE_PID_SAVE = None
	zencad.gui.signal_handling.setup_simple_interrupt_handling()

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--info", action="store_true")
	parser.add_argument('-v', "--debug", action="store_true")
	parser.add_argument("--version", action="store_true")
	parser.add_argument("--pyservoce-version", action="store_true")
	parser.add_argument("-I", "--mpath", action="store_true")
	parser.add_argument("-m", "--module", default="zencad")
	parser.add_argument("--subproc", action="store_true")
	parser.add_argument("--replace", action="store_true")
	parser.add_argument("--widget", action="store_true")
	parser.add_argument("--prescale", action="store_true")
	parser.add_argument("--sleeped", action="store_true", help="Don't use manualy. Create sleeped thread.")
	#parser.add_argument("--no-daemon", action="store_true")
	parser.add_argument("--no-show", action="store_true")
	parser.add_argument("--no-sleeped", action="store_true")
	parser.add_argument("--no-screen", action="store_true")
	parser.add_argument("--no-evalcache-notify", action="store_true")
	parser.add_argument("--no-embed", action="store_true")
	parser.add_argument("--no-cache", action="store_true")
	parser.add_argument("--size")
	parser.add_argument("--no-restore", action="store_true")
	parser.add_argument("--tgtpath")
	parser.add_argument("--debugcomm", action="store_true")
	parser.add_argument("--session_id", type=int, default=0)
	parser.add_argument("paths", type=str, nargs="*", help="runned file")
	pargs = parser.parse_args()

	if hasattr(pargs,"tgtpath") and pargs.tgtpath: pargs.tgtpath = protect_path(pargs.tgtpath)
	if len(pargs.paths) > 0: pargs.paths[0] = protect_path(pargs.paths[0])

	if pargs.module != "zencad":
		print("module opt is not equal 'zencad'")

	if pargs.version:
		print(zencad.version.__version__)
		sys.exit(0)

	if pargs.pyservoce_version:
		print(zencad.version.__pyservoce_version__)
		sys.exit(0)

	if pargs.debug:
		zencad.configure.verbose(True)

	if pargs.info:
		zencad.configure.info(True)

	if pargs.no_sleeped:
		zencad.configure.CONFIGURE_SLEEPED_OPTIMIZATION = False

	if pargs.no_cache:
		zencad.configure.CONFIGURE_DISABLE_LAZY=True
		zencad.lazifier.disable_lazy()

	if pargs.no_screen:
		zencad.configure.CONFIGURE_SCREEN_SAVER_TRANSLATE = False

	if pargs.debugcomm:
		zencad.configure.CONFIGURE_PRINT_COMMUNICATION_DUMP = True

	if pargs.no_evalcache_notify:
		zencad.configure.CONFIGURE_WITHOUT_EVALCACHE_NOTIFIES = True

	if pargs.no_embed:
		zencad.configure.CONFIGURE_NO_EMBEDING_WINDOWS = True

	if pargs.no_restore:
		zencad.configure.CONFIGURE_NO_RESTORE = True


	trace(f"__MAIN__ ({os.getpid()})", sys.argv)
	trace(pargs)

	if pargs.mpath:
		print(zencad.moduledir)
		return

	pargs.nodaemon = True

	# Подчинённый режим работы gui. 
	# Используется при создании gui из в ходе работы интерпретатора.
	if pargs.subproc:
		if pargs.tgtpath == None:
			print_to_stderr("Error: subproc mode without tgtpath")
			exit(0)

		trace("start_main_application")
		zencad.gui.application.start_main_application(pargs.tgtpath, display_mode=True, console_retrans=True)	
		trace("start_main_application ... ok")
		return

	retrans_out_file = None
	if pargs.replace and zencad.configure.CONFIGURE_CONSOLE_RETRANSLATE:
		# Теперь можно сделать поток для обработки данных, которые программа собирается 
		# посылать в stdout
		zencad.gui.application.CONSOLE_RETRANS_THREAD = zencad.gui.retransler.console_retransler(sys.stdout)
		zencad.gui.application.CONSOLE_RETRANS_THREAD.start()
		retrans_out_file = zencad.gui.application.CONSOLE_RETRANS_THREAD.new_file

	if pargs.sleeped:
		# Эксперементальная функциональность для ускорения обновления модели. 
		# Процесс для обновления модели создаётся заранее и ждёт, пока его пнут со стороны сервера.
		zencad.util.PROCNAME = f"sl({os.getpid()})"
		readFile = os.fdopen(zencad.gui.application.STDIN_FILENO)

		while 1:
			trace("SLEEPED THREAD: read")
			rawdata = readFile.readline()
			try:
				data = pickle.loads(base64.b64decode(bytes(rawdata, "utf-8")))
				trace("SLEEPED THREAD RECV:", data)
			except:
				print_to_stderr("Unpickle error", rawdata)
				sys.exit(0)			
	
			if "cmd" in data and data["cmd"] == "stopworld":
				sys.exit(0)
				return
	
			if "cmd" in data and data["cmd"] == "set_opposite_pid":
				OPPOSITE_PID_SAVE = data["data"]
				continue

			break

		try:
			pargs.prescale = data["need_prescale"]
			pargs.size = data["size"]
			pargs.paths = [data["path"]]
		except:
			print_to_stderr("Unpickle error_2", data)
			exit(0)

		zencad.settings.restore()			

	if pargs.replace and zencad.configure.CONFIGURE_CONSOLE_RETRANSLATE:
		# Теперь можно сделать поток для обработки данных, которые программа собирается 
		# посылать в stdout
		zencad.gui.application.MAIN_COMMUNICATOR = zencad.gui.communicator.Communicator(
			ifile=sys.stdin, ofile=retrans_out_file)
		zencad.gui.application.MAIN_COMMUNICATOR.start_listen()
		#zencad.gui.application.MAIN_COMMUNICATOR.newdata.connect(hard_finish_checker)
		
		if OPPOSITE_PID_SAVE is not None:
			zencad.gui.application.MAIN_COMMUNICATOR.set_opposite_pid(OPPOSITE_PID_SAVE)

		zencad.lazifier.install_evalcahe_notication(zencad.gui.application.MAIN_COMMUNICATOR)

		#zencad.gui.application.MAIN_COMMUNICATOR.send({"cmd":"clientpid", "pid":int(os.getpid())})
	


	if len(pargs.paths) == 0 and not pargs.sleeped:
		# Если программа вызывается без указания файла, создаём gui. 
		# Режим презентации указывает gui, что оно предоставлено само себе
		# и ему следует развлечь публику самостоятельно, не ожидая бинда виджета.
		if pargs.nodaemon:
			zencad.gui.application.start_main_application(presentation=True)
		else:
			# Windows?
			print("TODO ?")
			sys.exit(0)
			#subprocess.Popen("nohup python3 -m zencad --nodaemon > /dev/null 2>&1&", shell=True, stdout=None, stderr=None)
		
	else:
		# Режим работы, когда указан файл.
		# Политика такова, что начало исполняется вычисляемый 
		# скрипт, а потом, после вызова zencad.show,
		# применяются указанные варианты вызова.
		# информация отсюда транслируется функции show
		# через глобальные переменные.

		if not os.path.abspath(pargs.paths[0]):
			path = os.path.join(os.getcwd(), pargs.paths[0])
		else:
			path = pargs.paths[0]
		zencad.showapi.EXECPATH = path

		if os.path.splitext(pargs.paths[0])[1] == ".brep":
			zencad.gui.viewadaptor.brep_hot_open(pargs.paths[0])
			return
	
		# Устанавливаем рабочей директорией дирректорию,
		# содержащую целевой файл.
		# TODO: Возможно, так делать нужно только
		# при загрузке через GUI. Вынести флаг?
		directory = os.path.dirname(os.path.abspath(path))
		os.chdir(directory)
		
		sys.path.append(directory)
		
		# По умолчанию приложение работает в режиме,
		# предполагающем вызов указанного скрипта. 
		# Далее скрипт сам должен создать GUI через showapi.
		zencad.showapi.SHOWMODE = "makeapp"
		
		# Специальный режим, устанавливаемый GUI при загрузке скрипта.
		# Делает ребинд модели в уже открытом gui.
		# Информация об окне передаётся основному процессу через пайп.
		if pargs.replace:
			zencad.showapi.PRESCALE = pargs.prescale
			zencad.showapi.SESSION_ID = int(pargs.session_id)
			zencad.showapi.SHOWMODE = "replace"
	
		# Режим работы в котором виджет работает отдельно и не биндится в gui:
		if pargs.widget:
			zencad.showapi.SHOWMODE = "widget"

		if pargs.no_show:
			zencad.showapi.SHOWMODE = "noshow"

		if pargs.size:
			arr = pargs.size.split(',')
			zencad.showapi.SIZE = (int(arr[0]), int(arr[1]))

		try:
			runpy.run_path(path, run_name="__main__")
		except Exception as ex:
			print("Error: {}".format(ex))
			ex_type, ex, tb = sys.exc_info()
			print("\r\n".join(traceback.format_exception(ex_type, ex, tb)))
			zencad.gui.application.MAIN_COMMUNICATOR.send({"cmd":"fault"})
			time.sleep(0.1)
			return -1

	return 0
	
	trace("AFTER RUNPY")

def main():
	sts = do_main()
	finish_procedure()
	trace("EXIT")
	sys.exit(sts)

if __name__ == "__main__":
	zencad.util.set_process_name("zencad")
	main()

	
