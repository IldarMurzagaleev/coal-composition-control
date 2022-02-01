from pathlib import Path
from typing import Dict, Union

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from numpy.typing import NDArray

from mask_rcnn import MaskRCNN
from src.converters.mask_to_vgg import masks2vgg


class Annotator(MaskRCNN):

    def names_and_masks(self, folder: Path) -> Dict[str, NDArray]:
        names_masks = {}
        for image_path in folder.glob('*'):
            img = cv2.imread(str(image_path))
            img = transforms.ToTensor()(img)
            img.to(self.device)

            prediction = self.model([img])
            masks = torch.squeeze(prediction[0]['masks'])
            masks = (masks > self.segmentation_th)
            names_masks[image_path.name] = np.array(masks)
        return names_masks

    def to_vgg(self, folder: Union[Path, str], save_path: Union[str, Path]) -> None:
        names_and_masks = self.names_and_masks(folder=Path(folder))
        masks2vgg(names_and_masks=names_and_masks, save_path=save_path)


if __name__ == '__main__':
    annotator = Annotator(
        weights='/home/ji411/PycharmProjects/comptech-coal-composition-control/mask-rcnn.pth',
        box_conf_th=0.7,
        nms_th=0.2,
        segmentation_th=0.7
    )
    annotator.to_vgg(
        folder='/home/ji411/PycharmProjects/comptech-coal-composition-control/few_data',
        save_path='/home/ji411/PycharmProjects/comptech-coal-composition-control/output.json'
    )
