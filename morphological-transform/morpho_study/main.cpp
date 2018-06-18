#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <string>

char MORPH_TYPES[7][25] = {
    "Erosion",
    "Dilation",
    "Opening",
    "Closing",
    "Morphological Gradient",
    "Top Hat",
    "Black Hat"
};

char KERNEL_SHAPES[3][25] = {
    "Rectangular",
    "Cross-shaped",
    "Elliptical"
};

char BLUR[2][5] = {
    "Off",
    "On"
};

struct MatWrapper {
    cv::Mat back;
    cv::Mat src;
    cv::Mat mask;
    cv::Mat maskSrc;
};

// #define CV_RGB(r, g, b) cv::Scalar((b), (g), (r), 0)

cv::Mat grayImage;

// adiciona um texto à tela
// o texto descreverá as operações feitas na imagem
void displayText(cv::Mat destImg, int mtId, int ksId, int ks, int blr) {

    char outBottom[80];
    char outTop[80];
    sprintf(outTop, "%s,  Blur: %s", MORPH_TYPES[mtId], BLUR[blr]);
    sprintf(outBottom, "%s kernel of size %d", KERNEL_SHAPES[ksId], ks);

    cv::putText(destImg, outTop, cv::Point(10,20), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

    cv::putText(destImg, outBottom, cv::Point(10,destImg.rows-10), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

}

// mostra a imagem cinza e seta todas as trackbars para o estado inicial
void displayGrayImg() {

    cv::setTrackbarPos("Kernel Size", "Morpho Something", 0);
    cv::setTrackbarPos("Kernel Shape", "Morpho Something", 0);

    cv::putText(grayImage, "Original Grayscale Image", cv::Point(10,20), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

    cv::imshow("Morpho Something", grayImage);
}

void showImg(void * data){

    // pega os valores das trackbars
    int kernelSize = (int)cv::getTrackbarPos("Kernel Size", "Morpho Something") + 1;
    int kernelShape = (int)cv::getTrackbarPos("Kernel Shape", "Morpho Something");
    int morphType = (int)cv::getTrackbarPos("Morph Type", "Morpho Something") - 1;
    int blurState = (int)cv::getTrackbarPos("Blur State", "Morpho Something");

    cv::Mat res;
    cv::Mat mask2 = ((MatWrapper*)data)->mask.clone();
    cv::Mat kernel = cv::getStructuringElement(kernelShape, cv::Size(kernelSize, kernelSize));


    // gray image
    if (morphType == -1) {
        displayGrayImg();
        return;

    // transformações morphológicas
    } else {
        cv::morphologyEx(mask2, res, morphType, kernel);

    }

    displayText(res, morphType, kernelShape, kernelSize, blurState);
    cv::imshow("Morpho Something", res);
}

// altera as opções de imagem
static void onTrackbar(int val, void* data) {

    showImg(data);

}

void applyMask(void * data) {

    cv::adaptiveThreshold(((MatWrapper*)data)->src, ((MatWrapper*)data)->maskSrc, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C,
                          cv::THRESH_BINARY, 115, 1);

    cv::copyMakeBorder(((MatWrapper*)data)->src, grayImage, 30, 30, 0, 0,
                       cv::BORDER_CONSTANT, cv::Scalar(0));

    cv::copyMakeBorder(((MatWrapper*)data)->maskSrc, ((MatWrapper*)data)->mask, 30, 30, 0, 0,
                       cv::BORDER_CONSTANT, cv::Scalar(0));

}

static void onBlur(int val, void* data) {

    if (val) {
        cv::Mat img;
        cv::GaussianBlur(((MatWrapper*)data)->src, img, cv::Size(3, 3), 0);

        ((MatWrapper*)data)->src = img.clone();

    } else {
        ((MatWrapper*)data)->src = ((MatWrapper*)data)->back.clone();
    }

    applyMask(data);
    showImg(data);

}

int main(int argc, char** argv) {

    cv::Mat src = cv::imread(argv[1], cv::IMREAD_GRAYSCALE);

    // guarda as posições das trackbars
    int trackPosA = 0;
    int trackPosB = 0;
    int trackPosC = 0;
    int trackPosD = 0;

    cv::Mat maskSrc;
    cv::Mat mask;

    struct MatWrapper MatSet;
    MatSet.back = src.clone();
    MatSet.src = src;
    MatSet.mask = mask;
    MatSet.maskSrc = maskSrc;

    void * data = (void*)(&MatSet);
    // cria a janela
    cv::namedWindow("Morpho Something", cv::WINDOW_AUTOSIZE);

    // cria a trackbar para alterar o tipo de kernel
    cv::createTrackbar("Kernel Shape", "Morpho Something", &trackPosA, 2,
                       onTrackbar, data);

    // cria a trackbar para alterar o tamanho do kernel
    cv::createTrackbar("Kernel Size", "Morpho Something", &trackPosB, 5,
                      onTrackbar, data);

    // cria a trackbar para alterar o tipo de transformação
    cv::createTrackbar("Morph Type", "Morpho Something", &trackPosC, 6,
                       onTrackbar, data);

    // cria a trackbar para ativar/desativar o blur
    cv::createTrackbar("Blur State", "Morpho Something", &trackPosD, 1,
                       onBlur, data);

    applyMask(data);
    displayGrayImg();

    cv::waitKey(0);

    return 0;
}
