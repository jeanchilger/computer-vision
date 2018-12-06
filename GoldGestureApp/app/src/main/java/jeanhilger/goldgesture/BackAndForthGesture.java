package jeanhilger.goldgesture;

public final class BackAndForthGesture {

    private double mMinDistance; //The minimum distance that defines a back and forth movement

    private double mStartPosition;
    private double mDelta;

    private int mBackCount;
    private int mForthCount;

    // constructor
    public BackAndForthGesture(final double minDistance) {
        this.mMinDistance = minDistance;
    }

    public int getBackAndForthCount() {
        return Math.min(this.mBackCount, this.mForthCount);
    }

    public void start(final double position) {
        this.mStartPosition = position;
        this.mDelta = 0;
        this.mBackCount = 0;
        this.mForthCount = 0;
    }

    public void update(final double position) {
        double lastDelta = this.mDelta;
        mDelta = position - this.mStartPosition;
        if (lastDelta < this.mMinDistance && this.mDelta >= this.mMinDistance) {
            this.mForthCount++;

        } else if (lastDelta > -this.mMinDistance && mDelta <= -this.mMinDistance) {
            this.mBackCount++;
        }
    }

    public void resetCounts() {
        this.mForthCount = 0;
        this.mBackCount = 0;
    }
}
