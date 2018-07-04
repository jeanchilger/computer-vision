// g++ main.cpp `pkg-config --cflags --libs opencv` -std=c++11

#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <string>

// matrixes with the labels
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
    cv::Mat back; // backup of the original gray image;
    cv::Mat src; // the source that will be used to apply the morph;
    cv::Mat maskSrc; // the mask where the adaptiveThreshold is applied;
    cv::Mat mask; // the mask like maskSrc but with borders;
    cv::Mat res; // the final answer, just to allow saving the image;
};

// #define CV_RGB(r, g, b) cv::Scalar((b), (g), (r), 0)

cv::Mat grayImage;

// text on screen
void makeText(cv::Mat destImg, int mtId, int ksId, int ks, int blr) {

    char outBottom[80];
    char outTop[80];
    sprintf(outTop, "%s,  Blur: %s", MORPH_TYPES[mtId], BLUR[blr]);
    sprintf(outBottom, "%s kernel of size %d", KERNEL_SHAPES[ksId], ks);

    cv::putText(destImg, outTop, cv::Point(10,20), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

    cv::putText(destImg, outBottom, cv::Point(10,destImg.rows-10), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

}

// just show the original gray image
void displayGrayImg() {

    // cv::setTrackbarPos("Kernel Size", "Morpho Something", 0);
    // cv::setTrackbarPos("Kernel Shape", "Morpho Something", 0);

    cv::putText(grayImage, "Original Grayscale Image", cv::Point(10,20), cv::FONT_HERSHEY_DUPLEX, 0.7,
                cv::Scalar(200), 1, cv::LINE_AA);

    cv::imshow("Morpho Something", grayImage);
}

// shows the image - with the proper operations applied
void showImg(void * data){

    // trackbars values
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

    // morphology
    } else {
        cv::morphologyEx(mask2, res, morphType, kernel);

    }

    ((MatWrapper*)data)->res = res;

    makeText(res, morphType, kernelShape, kernelSize, blurState);
    cv::imshow("Morpho Something", res);
}

// gets the state of the trackbars
static void onTrackbar(int val, void* data) {

    showImg(data);

}

// applies the threshold and create borders at the image
void applyMask(void * data) {

    cv::adaptiveThreshold(((MatWrapper*)data)->src, ((MatWrapper*)data)->maskSrc, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C,
                          cv::THRESH_BINARY, 21, 2);

    cv::copyMakeBorder(((MatWrapper*)data)->src, grayImage, 30, 30, 0, 0,
                       cv::BORDER_CONSTANT, cv::Scalar(0));

    cv::copyMakeBorder(((MatWrapper*)data)->maskSrc, ((MatWrapper*)data)->mask, 30, 30, 0, 0,
                       cv::BORDER_CONSTANT, cv::Scalar(0));

}

// apply the gaussian blur to an image
static void onBlur(int val, void* data) {

    if (val) {
        cv::Mat img;
        cv::GaussianBlur(((MatWrapper*)data)->src, img, cv::Size(5, 5), 0);

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
    // create the window
    cv::namedWindow("Morpho Something", cv::WINDOW_AUTOSIZE);

    // kernel type
    cv::createTrackbar("Kernel Shape", "Morpho Something", &trackPosA, 2,
                       onTrackbar, data);

    // kernel size
    cv::createTrackbar("Kernel Size", "Morpho Something", &trackPosB, 5,
                      onTrackbar, data);

    // morphological transformation
    cv::createTrackbar("Morph Type", "Morpho Something", &trackPosC, 7,
                       onTrackbar, data);

    // blur
    cv::createTrackbar("Blur State", "Morpho Something", &trackPosD, 1,
                       onBlur, data);

    applyMask(data);
    MatSet.res = grayImage;
    displayGrayImg();

    int k;
    // gets the user key
    while (true) {
        k = cv::waitKey();
        if (k == 115) {
            cv::imwrite("image.png", MatSet.res);

        } else if (k == 27) {
            cv::destroyAllWindows();
            break;
        }
    }

    return 0;
}
