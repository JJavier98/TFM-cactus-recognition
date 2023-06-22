# Notas varias sobre experimentación

## Resnet50 preentrenadas VS no preentrenadas

No hay una diferencia notable entre utilizar ResNet50 preentrenada con imagenet o no. En los casos en los que una opción es mejor que otra parece ser fruto del carácter aleatorio de cada ejecución.  --> **ERROR**: no se inicializaba la red pero se cargaban los pesos desde archivo así que los resultados "no preentrenados" realmente sí lo estaban, de ahí que se parezcan tanto a los "sí preentrenados".

## ChatGPT

Mencionar la ayuda de ChatGPT para configurar ResNet18 como backbone y para realizar una aproximación a la implementación de ***EarlyStopping***.

## Resnet18

Entrenando ResNet18 en 20 épocas muestra una tendencia creciente al final del entrenamiento
por lo que entrenamos ahora hasta 50 épocas. Tras 50 épocas la tendencia sigue siendo creciente pero descartamos la opción no preentrenada. Entrenamos ahora durante 200 épocas. Más o menos en la época 65 se alcanza el máximo de mAP.

## Resnet101

Entrenando ResNet101 20 épocas muestra una tendencia creciente. La versión sin preentrenamiento no muestra un avance suficientemente bueno por lo que queda descartada. La versión preentrenada será evaluada de nuevo con un entrenamiento de 200 épocas. Sobre la época 40 se alcanza una asíntota horizontal en mAP.


