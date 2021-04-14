import time
import multiprocessing
from proxypool.processors.server import app
from proxypool.processors.getter import Getter
from proxypool.processors.tester import Tester
from proxypool.setting import CYCLE_GETTER, CYCLE_TESTER, API_HOST, API_THREADED, API_PORT, ENABLE_SERVER, \
    ENABLE_GETTER, ENABLE_TESTER, IS_WINDOWS
from loguru import logger


if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Scheduler():
    """
    调度器
    """
    
    def run_tester(self, cycle=CYCLE_TESTER):
        """
        run 测试器
        """
        if not ENABLE_TESTER:
            logger.info('检测器未启用，退出')
            return
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)
    
    def run_getter(self, cycle=CYCLE_GETTER):
        """
        run getter
        """
        if not ENABLE_GETTER:
            logger.info('getter未启用，退出')
            return
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)
    
    def run_server(self):
        """
        run api服务器
        """
        if not ENABLE_SERVER:
            logger.info('服务器未启用，退出')
            return
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
    
    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('正在启动ip代理池。。。。')
            # 检测器
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            # ip生成器
            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                logger.info(f'starting getter, pid{getter_process.pid}...')
                getter_process.start()

            # 服务器
            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)
                logger.info(f'starting server, pid{server_process.pid}...')
                server_process.start()
            
            tester_process.join()
            getter_process.join()
            server_process.join()
        except KeyboardInterrupt:
            logger.info('接收到的键盘中断信号')
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            getter_process.join()
            server_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('代理终止')


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
