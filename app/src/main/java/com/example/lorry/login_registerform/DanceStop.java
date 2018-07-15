package com.example.lorry.login_registerform;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;


public class DanceStop implements SensorEventListener {
    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private Sensor mGyroscope;
//  private MediaPlayer mMediaPlayer;
    private double initAcce=Double.NaN;
    private double initGyro=Double.NaN;
    private static final int GRACE=100;
    private int skips =GRACE;
    private Listener listener;
    static public boolean isMusicOn=false;
    private Handler handler;

    public DanceStop(Context context,@NonNull Listener callback){
        mSensorManager= (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
            if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null){
                mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            }
            else{
                throw new UnsupportedOperationException("No accelerometer hardware found");
            }
        if (mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) != null){
            mGyroscope = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        }
        else{
            Toast.makeText(context, "No accelerometer hardware found", Toast.LENGTH_SHORT).show();
        }
        listener=callback;
        handler=new Handler();
    }
    // set audio file from url or file
//    public void setMedia(String url){
//        mMediaPlayer=new MediaPlayer();
//        try {
//            mMediaPlayer.setDataSource(url);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        initMediaPlayer();
//    }
//    // set audio file from assets
//    public void setMedia(AssetFileDescriptor afd) throws IOException {
//        mMediaPlayer=new MediaPlayer();
//        mMediaPlayer.setDataSource(afd.getFileDescriptor(),afd.getStartOffset(),afd.getLength());
//        initMediaPlayer();
//    }
//    //inits media player
//    private void initMediaPlayer(){
//        mMediaPlayer.setOnCompletionListener((mediaPlayer -> {
//            mediaPlayer.stop();
//            try {
//                mediaPlayer.prepare();
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//            mediaPlayer.start();
//        }));
//        try {
//            mMediaPlayer.prepare();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//    }
    //game start signal , plays music and starts listening for sensors
    public void gameStart(){
        isMusicOn=true;
//        mMediaPlayer.start();
        handler.postDelayed(() -> {
           mSensorManager.registerListener(DanceStop.this, mAccelerometer, SensorManager.SENSOR_DELAY_FASTEST);
           if (mGyroscope != null)
               mSensorManager.registerListener(DanceStop.this, mGyroscope, SensorManager.SENSOR_DELAY_FASTEST);
       },1000);
    }

    //listen for sensor events and calc abs diff to find if player is moving or not....1 sec grace time for player to start dancing
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        if(skips ==0){
            if(listener!=null)
            {
                stopGame();
                listener.onResult(false);
            }
        }
        double mag=Math.sqrt(sensorEvent.values[0]*sensorEvent.values[0]+sensorEvent.values[1]*sensorEvent.values[1]+sensorEvent.values[2]*sensorEvent.values[2]);
        if(sensorEvent.sensor.getName().equals(mAccelerometer.getName()))
        {
            if(isMusicOn&&Math.abs(mag-initAcce)<0.1d)
                skips--;
            else if(!isMusicOn&&Math.abs(mag-initAcce)>0.5d)
                skips--;
            else
                skips =GRACE;

            initAcce=mag;
            Log.d("Accel",String.valueOf(initAcce));
        }
        else
            if(mGyroscope!=null)
            if(sensorEvent.sensor.getName().equals(mGyroscope.getName()))
            {
                if(isMusicOn&&Math.abs(mag-initGyro)<0.1d)
                    skips--;
                else if(!isMusicOn&&Math.abs(mag-initGyro)>0.5d)
                    skips--;
                else skips=GRACE;
                initGyro=mag;
                Log.d("Gyr",String.valueOf(initGyro));

            }
    }
    //required by interface not needed here
    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
    //interface needed for callback if lost or not
    public interface Listener{
        void onResult(boolean win);
    }
    //stop listening to sensor and stop music
    private void stopGame(){
//        mMediaPlayer.stop();
        mSensorManager.unregisterListener(this);

    }
    //game stop signal.... 1 sec grace time for player to stop
    public void gameStop(){
        stopGame();
        isMusicOn=false;
        handler.postDelayed(()->{
            if(skips>0&&listener!=null)
                listener.onResult(true);
        },1000);

    }
}

