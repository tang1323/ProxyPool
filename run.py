from proxypool.scheduler import Scheduler
import argparse


parser = argparse.ArgumentParser(description='ProxyPool')
parser.add_argument('--processor', type=str, help='processor to run')
args = parser.parse_args()

if __name__ == '__main__':
    # 如果设置了处理器，就运行它
    if args.processor:
        getattr(Scheduler(), f'run_{args.processor}')()
    else:
        Scheduler().run()
