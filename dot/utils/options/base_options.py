import argparse
import random
from datetime import datetime

# 将字符串转换为布尔值
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

#如何启用torch3d？
class BaseOptions:
    #执行程序的基本选项
    def initialize(self, parser):
        parser.add_argument("--name", type=str)
        parser.add_argument("--model", type=str, default="dot", choices=["dot", "of", "pt"])
        parser.add_argument("--datetime", type=str, default=None)
        parser.add_argument("--data_root", type=str)
        parser.add_argument("--height", type=int, default=512)
        parser.add_argument("--width", type=int, default=512)
        parser.add_argument("--aspect_ratio", type=float, default=1)
        parser.add_argument("--batch_size", type=int)
        #运行程序时追踪的点的数目，在demo options中被覆盖，设置为8192
        parser.add_argument("--num_tracks", type=int, default=2048)
        #如果设置为16，效果会远不如2048
        # parser.add_argument("--num_tracks", type=int, default=16)
        parser.add_argument("--sim_tracks", type=int, default=2048)
        # parser.add_argument("--sim_tracks", type=int, default=16)
        parser.add_argument("--alpha_thresh", type=float, default=0.8)
        #是否为训练模式
        parser.add_argument("--is_train", type=str2bool, nargs='?', const=True, default=False)

        # Parallelization
        parser.add_argument('--worker_idx', type=int, default=0)
        parser.add_argument("--num_workers", type=int, default=2)

        # Optical flow estimator
        parser.add_argument("--estimator_config", type=str, default="configs/raft_patch_8.json")
        parser.add_argument("--estimator_path", type=str, default="checkpoints/cvo_raft_patch_8.pth")
        parser.add_argument("--flow_mode", type=str, default="direct", choices=["direct", "chain", "warm_start"])

        # Optical flow refiner
        parser.add_argument("--refiner_config", type=str, default="configs/raft_patch_4_alpha.json")
        parser.add_argument("--refiner_path", type=str, default="checkpoints/movi_f_raft_patch_4_alpha.pth")

        # Point tracker
        parser.add_argument("--tracker_config", type=str, default="configs/cotracker_patch_4_wind_8.json")
        parser.add_argument("--tracker_path", type=str, default="checkpoints/movi_f_cotracker_patch_4_wind_8.pth")
        parser.add_argument("--sample_mode", type=str, default="all", choices=["all", "first", "last"])

        # Interpolation
        parser.add_argument("--interpolation_version", type=str, default="torch3d", choices=["torch3d", "torch"])
        return parser

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser = self.initialize(parser)
        args = parser.parse_args()
        #自动根据当前时间生成文件夹的名称
        if args.datetime is None:
            args.datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        name = f"{args.datetime}_{args.name}_{args.model}"
        if hasattr(args, 'split'):
            name += f"_{args.split}"
        args.checkpoint_path = f"checkpoints/{name}"
        args.log_path = f"logs/{name}"
        args.result_path = f"results/{name}"
        #什么是world_size？
        if hasattr(args, 'world_size'):
            args.batch_size = args.batch_size // args.world_size
            args.master_port = f'{10000 + random.randrange(1, 10000)}'
        return args
