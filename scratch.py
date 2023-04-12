from mmpose.apis import MMPoseInferencer

# create the inferencer using the model alias
inferencer = MMPoseInferencer(
    pose2d='models/td-hm_hrnet-w32_8xb64-210e_coco-256x192.py',
    pose2d_weights='models/td-hm_hrnet-w32_8xb64-210e_coco-256x192-81c58e40_20220909.pth'
)

# The MMPoseInferencer API employs a lazy inference approach,
# creating a prediction generator when given input
# for i in range(20):
#     img_path = 'data/swim2/images/frame_0000' + str(i).zfill(2) + '.PNG'  # replace this with your own image path
#     result_generator = inferencer(img_path, pred_out_dir='results/predictions', vis_out_dir='results/vis_results')
#     result = next(result_generator)
result_generator = inferencer("data/breast.mp4", pred_out_dir='results', vis_out_dir='results')
while True:
    try:
        result = next(result_generator)
    except StopIteration:
        break

# import os
#
# from mmpose.apis import inference_topdown, init_model
# from mmpose.utils import register_all_modules
#
# register_all_modules()
#
# config_file = 'models/td-hm_hrnet-w32_8xb64-210e_coco-256x192.py'
# checkpoint_file = 'models/td-hm_hrnet-w32_8xb64-210e_coco-256x192-81c58e40_20220909.pth'
# model = init_model(config_file, checkpoint_file, device='cuda:0')  # or device='cpu'
#
# for file in os.listdir("data/swim2/images/"):
#     print(file)
#     # test a single image
#     # please prepare an image with person
#     results = inference_topdown(model, 'data/swim2/images/' + file)
#
#     # show the results
#
#     res = vis_pose_result(pose_model, 'data/swim2/images/' + file, pose_results, out_file='images_output/' + file)