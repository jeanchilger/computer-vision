package jeanhilger.goldgesture;

import android.provider.ContactsContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.LinkedList;
import java.util.List;

import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.view.Window;
import android.view.WindowManager;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewFrame;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewListener2;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.MatOfFloat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.opencv.objdetect.Objdetect;
import org.opencv.video.Video;


public final class CameraActivity extends AppCompatActivity implements CvCameraViewListener2 {

    private static final String TAG = "CameraActivity";

    // Variables to help in face detection:
    private static final double SCALE_FACTOR = 1.2;
    private static final double MIN_SIZE_PROPORTIONAL = 0.25;
    private static final double MAX_SIZE_PROPORTIONAL = 1.00;
    private static final int MIN_NEIGHBORS = 3;
    private static final int FLAGS = Objdetect.CASCADE_SCALE_IMAGE;

    // The proportion of the image to be excluded to assure that
    // the features are detected in the face (and not in some random background behind the face)
    private static final double MASK_PADDING_PROPORTIONAL = 0.15;

    // Face tracking
    private static final int MIN_FEATURES = 10;
    private static final int MAX_FEATURES = 80;
    private static final double MIN_FEATURE_QUALITY = 0.5;
    private static final double MIN_FEATURE_DISTANCE = 4.0;
    private static final float MAX_FEATURE_ERROR = 200f;

    // Gesture detection
    private static final double MIN_SHAKE_DIST_PROPORTIONAL = 0.04;
    private static final double MIN_NOD_DIST_PROPORTIONAL = 0.005;
    private static final int MIN_BACK_AND_FORTH_COUNT = 2;

    // Camera view
    private CameraBridgeViewBase mCameraView;

    // Dimensions of the original image
    private double mImageWidth;
    private double mImageHeight;

    // The current gray image
    private Mat mGrayUnoriented;

    // The current and  previous equalized gray images
    private Mat mEqualizedGray;
    private Mat mLastEqualizedGray;

    // Mask: the face is white and the background is black
    private Mat mMask;
    private Scalar mMaskForegroundColor;
    private Scalar mMaskBackgroundColor;

    // Face detector and some detection parameters
    private CascadeClassifier mFaceDetector;
    private Size mMinSize;
    private Size mMaxSize;
    private MatOfRect mFaces;

    // Initial features (before tracking)
    private MatOfPoint mInitialFeatures;

    // Current and previous features being tracked
    private MatOfPoint2f mFeatures;
    private MatOfPoint2f mLastFeatures;

    // Status and errors
    private MatOfByte mFeatureStatuses;
    private MatOfFloat mFeatureErrors;

    // If the face was being tracked
    private boolean mWasTrackingFace;

    // Colors for drawing
    private Scalar mFaceRectColor;
    private Scalar mFeatureColor;

    // Gesture detectors
    private BackAndForthGesture mNodHeadGesture;
    private BackAndForthGesture mShakeHeadGesture;

    // The audio for 20 questions
    //private YesNoAudioTree mAudioTree;

    // THE OPENCV LOADER CALLBACK
    private BaseLoaderCallback mLoaderCallback =
            new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(final int status) {
            switch(status) {
                case LoaderCallbackInterface.SUCCESS:
                    Log.d(TAG, "Opencv loadded succesfully");
                    mCameraView.enableView();
                    break;
                default:
                    super.onManagerConnected(status);
                    break;
            }
        }
    };

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        final Window window = getWindow();
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.activity_camera);
        this.mCameraView = (CameraBridgeViewBase) findViewById(R.id.camera_view);
        this.mCameraView.setCvCameraViewListener(this);
    }

    @Override
    public void onPause() {
        if (this.mCameraView != null) {
            this.mCameraView.disableView();
        }
        /*if (mAudioTree != null) {
            mAudioTree.stop();
        }*/
        resetGestures();
        super.onPause();
    }

    @Override
    public void onResume() {
        super.onResume();
        OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_4_0, this, mLoaderCallback);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (this.mCameraView != null) {
            this.mCameraView.disableView();
        }
        /*if (mAudioTree != null) {
            mAudioTree.stop();
        }*/
        resetGestures();
    }

    @Override
    public void onCameraViewStarted(final int width, final int height) {
        this.mImageHeight = height;
        this.mImageWidth = width;

        // Initialize the face detection variables
        initFaceDetector();
        mFaces = new MatOfRect();

        final int smallerSide;
        if (height < width) {
            smallerSide = height;

        } else {
            smallerSide = width;
        }

        final double minSizeSide = this.MIN_SIZE_PROPORTIONAL * smallerSide;
        this.mMinSize = new Size(minSizeSide, minSizeSide);

        final double maxSizeSide = this.MAX_SIZE_PROPORTIONAL * smallerSide;
        this.mMaxSize = new Size(maxSizeSide, maxSizeSide);

        // Matrices related to features
        this.mInitialFeatures = new MatOfPoint();
        this.mFeatures = new MatOfPoint2f(new MatOfPoint());
        this.mLastFeatures = new MatOfPoint2f(new MatOfPoint());
        this.mFeatureStatuses = new MatOfByte();
        this.mFeatureErrors = new MatOfFloat();

        // Colors for drawing in screen
        this.mFaceRectColor = new Scalar(255.0, 0.0, 0.0);
        this.mFeatureColor = new Scalar(0.0, 255.0, 0.0);

        // Variables related to NOD and SHAKE movement;
        final double minShakeDist = minSizeSide * this.MIN_SHAKE_DIST_PROPORTIONAL;
        this.mShakeHeadGesture = new BackAndForthGesture(minShakeDist);

        final double minNodDist = minShakeDist * this.MIN_NOD_DIST_PROPORTIONAL;
        this.mNodHeadGesture = new BackAndForthGesture(minNodDist);

        // starts the audio
        /*mAudioTree = new YesNoAudioTree(this);
        mAudioTree.start();*/

        this.mGrayUnoriented = new Mat(height, width, CvType.CV_8UC1);

        this.mEqualizedGray = new Mat(width, height, CvType.CV_8UC1);
        this.mLastEqualizedGray = new Mat(width, height, CvType.CV_8UC1);

        this.mMask = new Mat(width, height, CvType.CV_8UC1);
        this.mMaskForegroundColor = new Scalar(255.0);
        this.mMaskBackgroundColor = new Scalar(0.0);

    }

    @Override
    public void onCameraViewStopped() {

    }

    @Override
    public Mat onCameraFrame (final CvCameraViewFrame inputFrame) {
        final Mat rgba = inputFrame.rgba();

        // Make the image in the portrait orientation and equalize it
        Imgproc.cvtColor(rgba, this.mGrayUnoriented, Imgproc.COLOR_RGBA2GRAY);
        Core.transpose(this.mGrayUnoriented, this.mEqualizedGray);
        Core.flip(this.mEqualizedGray, this.mEqualizedGray, -1);
        Imgproc.equalizeHist(this.mEqualizedGray, this.mEqualizedGray);

        final List<Point> featuresList;
        this.mFaceDetector.detectMultiScale(this.mEqualizedGray, this.mFaces, this.SCALE_FACTOR,
                this.MIN_NEIGHBORS, this.FLAGS, this.mMinSize, this.mMaxSize);

        if (mFaces.rows() > 0) {

            // First detected face.
            final double[] face = this.mFaces.get(0, 0);
            double minX = face[0];
            double minY = face[1];
            double width = face[2];
            double height = face[3];
            double maxX = minX + width;
            double maxY = minY + height;

            // Draw it
            Imgproc.rectangle(rgba, new Point(this.mImageWidth - minY, this.mImageHeight - minX),
                    new Point(this.mImageWidth - maxY, this.mImageHeight - maxX), this.mFaceRectColor);

            // Mask for face region
            double smallerSide;
            if (height < width) {
                smallerSide = height;
            } else {
                smallerSide = width;
            }

            double maskPadding = smallerSide * this.MASK_PADDING_PROPORTIONAL;
            this.mMask.setTo(this.mMaskBackgroundColor);

            Imgproc.rectangle(this.mMask, new Point(minX + maskPadding, minY + maskPadding),
                    new Point(maxX - maskPadding, maxY - maskPadding), this.mMaskForegroundColor,
                    -1);

            // Find the features in the face region
            Imgproc.goodFeaturesToTrack(this.mEqualizedGray, this.mInitialFeatures, this.MAX_FEATURES,
                    this.MIN_FEATURE_QUALITY, this.MIN_FEATURE_DISTANCE, this.mMask,
                    3, false, 0.04);

            this.mFeatures.fromArray(this.mInitialFeatures.toArray());
            featuresList = this.mFeatures.toList();

            if (this.mWasTrackingFace) {
                updateGestureDetection();
            } else {
                startGestureDetection();
            }
            this.mWasTrackingFace = true;

        } else {
            Video.calcOpticalFlowPyrLK(this.mLastEqualizedGray, this.mEqualizedGray, this.mLastFeatures,
                    this.mFeatures, this.mFeatureStatuses, this.mFeatureErrors);

            // Filter the features
            featuresList = new LinkedList<Point>(this.mFeatures.toList());
            final LinkedList<Byte> featureStatusesList = new LinkedList<Byte>(this.mFeatureStatuses.toList());
            final LinkedList<Float> featureErrorsList = new LinkedList<Float>(this.mFeatureErrors.toList());
            for (int i = 0; i < featuresList.size(); ) {
                if (featureStatusesList.get(i) == 0 ||
                        featureErrorsList.get(i) > MAX_FEATURE_ERROR) {
                    featuresList.remove(i);
                    featureStatusesList.remove(i);
                    featureErrorsList.remove(i);
                } else {
                    i++;
                }
            }

            // If remaining filters are too small the features are all discard
            if (featuresList.size() < MIN_FEATURES) {
                // The number of remaining features is too low; we have
                // probably lost the target completely.
                // Discard the remaining features.
                featuresList.clear();
                this.mFeatures.fromList(featuresList);
                this.mWasTrackingFace = false;
            } else {
                this.mFeatures.fromList(featuresList);
                updateGestureDetection();
            }
        }

        // Draw the current features.
        for (int i = 0; i< featuresList.size(); i++) {
            final Point p = featuresList.get(i);
            final Point pTrans = new Point(
                    this.mImageWidth - p.y,
                    this.mImageHeight - p.x);
            Imgproc.circle(rgba, pTrans, 8, this.mFeatureColor);
        }

        // Swap the references for current and previous images
        final Mat swapEqualizedGray = this.mLastEqualizedGray;
        this.mLastEqualizedGray = this.mEqualizedGray;
        this.mEqualizedGray = swapEqualizedGray;

        // Swap the features
        final MatOfPoint2f swapFeatures = this.mLastFeatures;
        this.mLastFeatures = this.mFeatures;
        this.mFeatures = swapFeatures;

        Core.flip(rgba, rgba, 1);
        return rgba;
    }

    private void startGestureDetection() {
        double[] featuresCenter = Core.mean(this.mFeatures).val;

        // Moving in X axis means a SHAKE with the head
        this.mShakeHeadGesture.start(featuresCenter[0]);

        // Moving in Y axis means a NOD with the head
        this.mNodHeadGesture.start(featuresCenter[1]);
    }

    private void updateGestureDetection() {
        final double[] featuresCenter = Core.mean(this.mFeatures).val;

        // Moving in X axis means a SHAKE with the head
        this.mShakeHeadGesture.update(featuresCenter[0]);
        final int shakeBackAndForthCount = this.mShakeHeadGesture.getBackAndForthCount();
        final boolean shakingHead = (shakeBackAndForthCount >= this.MIN_BACK_AND_FORTH_COUNT);

        // Moving in Y axis means a NOD with the head
        this.mNodHeadGesture.update(featuresCenter[1]);
        final int nodBackAndForthCount = this.mNodHeadGesture.getBackAndForthCount();
        final boolean noddingHead = (nodBackAndForthCount >= this.MIN_BACK_AND_FORTH_COUNT);

        if (shakingHead && noddingHead) {
            // shaking and nodding at same time? Ignore it.
            resetGestures();
        } else if (shakingHead) {
            //mAudioTree.takeNoBranch();
            resetGestures();
        } else if (noddingHead) {
            //mAudioTree.takeYesBranch();
            resetGestures();
        }
    }

    private void resetGestures() {
        if (this.mNodHeadGesture != null) {
            this.mNodHeadGesture.resetCounts();
        } else if (this.mShakeHeadGesture != null) {
            this.mShakeHeadGesture.resetCounts();
        }
    }

    private void initFaceDetector() {
        try {
            // Load Cascade file from res
            InputStream is = getResources().openRawResource(R.raw.lbpcascade_frontalface);
            File cascadeDir = getDir("cascade", Context.MODE_PRIVATE);
            File cascadeFile = new File (cascadeDir, "lbpcascade_frontalface.xml");
            FileOutputStream os = new FileOutputStream(cascadeFile);

            byte[] buffer = new byte[4096];
            int bytesRead;

            while ((bytesRead = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            is.close();
            os.close();

            this.mFaceDetector = new CascadeClassifier(cascadeFile.getAbsolutePath());
            if (this.mFaceDetector.empty()) {
                Log.e(TAG, "Failed to load cascade");
                finish();
            } else {
                Log.i(TAG, "Load cascade from " + cascadeFile.getAbsolutePath());
            }

            cascadeDir.delete();

        } catch (IOException e) {
            e.printStackTrace();
            Log.e(TAG, "Failed to load cascade. Exception thrown: " + e);
            finish();
        }
    }
}
