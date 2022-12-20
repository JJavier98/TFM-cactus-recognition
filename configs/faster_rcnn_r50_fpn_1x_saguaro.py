# The new config inherits a base config to highlight the necessary modification
_base_ = 'faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1),
        #mask_head=dict(num_classes=1)
        )
    )

# Modify dataset related settings
dataset_type = 'COCODataset'
classes = ('Cactus',)  # 'cactus 1 brazo','cactus 2 brazos','cactus 3+ brazos',)
data = dict(
    train=dict(
        img_prefix='data/imgs/google_maps/gm_saguaro_z21_train',
        classes=classes,
        ann_file='data/coco_annotations/saguaro/train/annotation_coco.json'),
    val=dict(
        img_prefix='data/imgs/google_maps/gm_saguaro_z21_val',
        classes=classes,
        ann_file='data/coco_annotations/saguaro/val/annotation_coco.json'),
    test=dict(
        img_prefix='data/imgs/google_maps/gm_saguaro_z21_test',
        classes=classes,
        ann_file='data/coco_annotations/saguaro/val/annotation_coco.json'))

# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = 'checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'