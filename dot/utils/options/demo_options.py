from .base_options import BaseOptions, str2bool

# demo.py的参数
#会覆盖base_options.py中的参数
#意面模式(spaghetti_last_mode)更适合包含上下运动的物体的视频
#覆盖模式(overlay)更适合包含左右运动的物体的视频
class DemoOptions(BaseOptions):
    def initialize(self, parser):
        BaseOptions.initialize(self, parser)
        parser.add_argument("--visualization_modes", type=str, nargs="+", default=["overlay", "spaghetti_last_static"])
        parser.add_argument("--video_path", type=str, default="orange.mp4")
        parser.add_argument("--mask_path", type=str, default="orange.png")
        parser.add_argument("--save_tracks", type=str2bool, nargs='?', const=True, default=False)
        parser.add_argument("--recompute_tracks", type=str2bool, nargs='?', const=True, default=False)
        parser.add_argument("--overlay_factor", type=float, default=0.75)
        parser.add_argument("--rainbow_mode", type=str, default="left_right", choices=["left_right", "up_down"])
        parser.add_argument("--save_mode", type=str, default="video", choices=["image", "video"])
        parser.add_argument("--spaghetti_radius", type=float, default=1.5)
        parser.add_argument("--spaghetti_length", type=int, default=40)
        parser.add_argument("--spaghetti_grid", type=int, default=30)
        parser.add_argument("--spaghetti_scale", type=float, default=2)
        parser.add_argument("--spaghetti_every", type=int, default=10)
        parser.set_defaults(data_root="datasets/demo", name="demo", batch_size=16, height=480, width=856, num_tracks=8192)
        return parser