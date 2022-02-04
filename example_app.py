import cv2

from constants import EXAMPLE_IMG, WEIGHTS_DIR
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN

if __name__ == '__main__':
    image = cv2.imread(str(EXAMPLE_IMG))

    if image is None:
        raise FileNotFoundError('check path to image')

    edge_segmentation = EdgeSegmentation(WEIGHTS_DIR / 'edge_segmentation.pth', width=1280, height=640)
    image = cv2.resize(image, (1280, 640), interpolation=cv2.INTER_AREA)
    coals = edge_segmentation.predict(image)
    print([coal.get_fraction() for coal in coals])

    mask_rcnn = MaskRCNN(WEIGHTS_DIR / 'mask_rcnn.pth')
    coals = mask_rcnn.predict(image)
    print([coal.get_fraction() for coal in coals])

    if coals:
        cv2.imshow('Contours', coals[0].plot_on(image))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
