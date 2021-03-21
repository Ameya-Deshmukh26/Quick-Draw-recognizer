from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import datasets, transforms
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np




class customDatasetClass(Dataset):

    def __init__(self, path ):

        """
        Custom Dataset Iterator class using Pytorch DataLoader
        :param path: Path to the directory containing the images
        Data
        ├───Class0
        │       image0.png
        │       image1.png
        │       image2.png
        │       image3.png
        │
        ├───Class1
        │       image0.png
        │       image1.png
        │       image2.png
        │       image3.png
        │
        ├───Class2
        │       image0.png
        │       image1.png
        │       image2.png
        │       image3.png
        │
        └───Class3
                image0.png
                image1.png
                image2.png
                image3.png
        """

        self.path = path
        self.allImagePaths = []
        self.allTargets = []
        self.targetToClass = sorted(os.listdir(self.path))

        for targetNo, targetI in enumerate(self.targetToClass):
            for i in sorted(os.listdir(self.path + '/' + targetI )):                             
                for images in sorted(os.listdir(self.path + '/' + targetI +'/'+ i )) :                    
                    self.allImagePaths.append(self.path + '/' + targetI + '/'+i+'/' + images)
                    self.allTargets.append(targetNo)
                                  
                

        # print(self.allImagePaths[0])
        # print(self.allTargets[0])
              
        self.transforms = torchvision.transforms.Compose([
            
            torchvision.transforms.ToTensor(),
            #torchvision.transforms.RandomAffine(10,translate=(0,0.1),scale=(1,1.1),shear=1.1),
            transforms.Normalize((0.1307,), (0.3081,))
            
            # torchvision.transforms.Normalize((0.1307,), (0.3081,))


        ])

    def __getitem__(self, item):
        
        image = Image.fromarray(plt.imread(self.allImagePaths[item])[:, :, 3])
        image = (np.array(image) > 0.1).astype((np.float32))
        # image = Image.open(self.allImagePaths[item]).convert('RGB')
       
        # print(image.shape)
        # exit(0)
        target = self.allTargets[item]

        image = self.transforms(image)
        #image = (np.array(image) > 0.1).astype((np.float32))[None, :, :]
        # image=image.reshape(1,384,384)
        # print(image.shape)
        # exit(0)
       

        return image, target

    def __len__(self):
        

        return len(self.allImagePaths)


if __name__ == "__main__":

    customDataLoaderObject = DataLoader(
        customDatasetClass(r'C:/Users/ameya/Documents/flask/GoogleDataImages_train'),
        batch_size=4,
        
        num_workers=8,
        shuffle=True,
    )

    #try printing this
    # for no,(images,target)in enumerate(customDataLoaderObject):
    #     print(images.shape)
    #     exit(0)
    #     for imageI in images:
    #         plt.imshow(imageI.numpy().transpose(1, 2, 0))
    #         plt.show()
    #         exit(0)

            
        # [4, 3, 256, 256], [4]