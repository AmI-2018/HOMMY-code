package com.example.lorry.login_registerform;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.AudioTrack;
import android.media.MediaRecorder;
import android.os.Handler;
import android.os.Process;
import android.util.Log;

import com.paramsen.noise.Noise;
import com.paramsen.noise.NoiseOptimized;

import java.nio.FloatBuffer;
import java.nio.ShortBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class VoiceHzDetector {
    //private int frequency;
    private final int SAMPLE_RATE = 44100;
    private String LOG_TAG="VoiceHzDetector";
    private Handler handler;

    private boolean mShouldContinue=false;
    private boolean isPlaying=false;
    private List<short[]> shorts;

    //private short[] frequencySamples;
    //private int sampleCount;


    //Initialized with the frequency of this match
    public VoiceHzDetector(){           //int freq){
        //frequency=freq;
        handler=new Handler();
        shorts=new ArrayList<>();

        //sampleCount = (int)(SAMPLE_RATE * 2.0 * (1 / 1000.0)) & ~1;
        //frequencySamples = getSineWave(frequency, sampleCount);

    }
    //generate the player for the current tone frequency
   /* private AudioTrack generateTonePlayer()
    {
        AudioTrack track = new AudioTrack(AudioManager.STREAM_MUSIC, SAMPLE_RATE,
                AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT,
                sampleCount * (Short.SIZE / 8), AudioTrack.MODE_STATIC);
        track.write(frequencySamples, 0, sampleCount);
        return track;
    }*/
    //generate sine wave tone for specified frequency
    /*private short[] getSineWave(double freqHz, int count) {
        short[] samples = new short[count];
        for(int i = 0; i < count; i += 1){
            short sample = (short)(Math.sin(2 * Math.PI * i / (44100.0 / freqHz)) * 0x7FFF);
            samples[i] = sample;
        }
        return samples;
    }*/
    //play the generated tone
    /*public void playHz(){
        generateTonePlayer().play();
       isPlaying=true;
       handler.postDelayed(()->isPlaying=false,1000);

    }*/
    //start recording pcm audio from mic unill @stopRecTone is called
    public void startRecTone(){
        if(isPlaying) return;
        mShouldContinue=true;
//        handler.postDelayed(()->mShouldContinue=false,5000);
        new Thread(new Runnable() {
            @Override
            public void run() {
                Process.setThreadPriority(Process.THREAD_PRIORITY_AUDIO);

                // buffer size in bytes
                int bufferSize = AudioRecord.getMinBufferSize(SAMPLE_RATE,
                        AudioFormat.CHANNEL_IN_MONO,
                        AudioFormat.ENCODING_PCM_16BIT);

                if (bufferSize == AudioRecord.ERROR || bufferSize == AudioRecord.ERROR_BAD_VALUE) {
                    bufferSize = SAMPLE_RATE * 2;
                }

                short[] audioBuffer = new short[bufferSize / 2];

                AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.MIC,
                        SAMPLE_RATE,
                        AudioFormat.CHANNEL_IN_MONO,
                        AudioFormat.ENCODING_PCM_16BIT,
                        bufferSize);

                if (record.getState() != AudioRecord.STATE_INITIALIZED) {
                    Log.e(LOG_TAG, "Audio Record can't initialize!");
                    return;
                }
                record.startRecording();

                Log.v(LOG_TAG, "Start recording");

                long shortsRead = 0;
                while (mShouldContinue) {
                    int numberOfShort = record.read(audioBuffer, 0, audioBuffer.length);
                    shortsRead += numberOfShort;
                    if(numberOfShort==audioBuffer.length)
                        shorts.add(audioBuffer.clone());
                    else
                    {
                        shorts.add(Arrays.copyOfRange(audioBuffer,0,numberOfShort));

                    }
                }

                record.stop();
                record.release();
                Log.v(LOG_TAG, String.format("Recording stopped. Samples read: %d", shortsRead));
            }
        }).start();
    }
    //stop recording from user mic
    public void stopRecTone(){
        mShouldContinue=false;
    }

    //analyze the user audio input and find the frequency of the voice ( using DFT )
    //should be called only after audio was recorded from mic
    public int analizeFrequency(){
        int size=0;
        if(shorts.size()==0) throw new IllegalStateException("Should record before analyzing frequency!!");
        for(short[] shortA:shorts)
            size+=shortA.length;
        double log=Math.log(size)/Math.log(2);
        size= log == (int) log ?size: (int) Math.pow(2, Math.floor(log));
        NoiseOptimized noise=Noise.real().optimized().init(size,true);

        float[] doubles=new float[size];
        FloatBuffer buffer=FloatBuffer.wrap(doubles);
        for(short[] shortA:shorts)
            for(int i=0;i<shortA.length &&buffer.position()<buffer.limit();i++)
                buffer.put(shortA[i]/32767.0f);
          float[] fft=noise.fft(doubles);
        double mag[] = new double[fft.length/2];
        for(int i = 0; i < fft.length; i+=2){

            mag[i/2] = Math.sqrt(fft[i]*fft[i]+fft[i+1]*fft[i+1]);
        }

        double peak = -1.0;
        int index=-1;
        for(int i = 0; i < mag.length; i++){
            if(peak < mag[i]){
                index=i;
                peak= mag[i];
            }
        }
        double frequency = Math.round((SAMPLE_RATE * index*1.0) /size);
        return (int) frequency;
    }
    //replay the tone recorded by the user
    //should be called only after audio was recorded from mic
    public void playTone(){

        if(mShouldContinue) return;
        int size=0;
        if(shorts.size()==0) throw new IllegalStateException("Should record before playing audio!!");

        for(short[] shortA:shorts)
            size+=shortA.length;
        ShortBuffer mSamples=ShortBuffer.allocate(size);
        for(short[] shortA:shorts)
            mSamples.put(shortA);

        int mNumSamples=mSamples.limit();
        new Thread(new Runnable() {
            @Override
            public void run() {
                int bufferSize = AudioTrack.getMinBufferSize(SAMPLE_RATE, AudioFormat.CHANNEL_OUT_MONO,
                        AudioFormat.ENCODING_PCM_16BIT);
                if (bufferSize == AudioTrack.ERROR || bufferSize == AudioTrack.ERROR_BAD_VALUE) {
                    bufferSize = SAMPLE_RATE * 2;
                }

                AudioTrack audioTrack = new AudioTrack(
                        AudioManager.STREAM_MUSIC,
                        SAMPLE_RATE,
                        AudioFormat.CHANNEL_OUT_MONO,
                        AudioFormat.ENCODING_PCM_16BIT,
                        bufferSize,
                        AudioTrack.MODE_STREAM);

                audioTrack.play();

                Log.v(LOG_TAG, "Audio streaming started");

                short[] buffer = new short[bufferSize];
                mSamples.rewind();
                int limit = mNumSamples;
                int totalWritten = 0;
                while (mSamples.position() < limit) {
                    int numSamplesLeft = limit - mSamples.position();
                    int samplesToWrite;
                    if (numSamplesLeft >= buffer.length) {
                        mSamples.get(buffer);
                        samplesToWrite = buffer.length;
                    } else {
                        for (int i = numSamplesLeft; i < buffer.length; i++) {
                            buffer[i] = 0;
                        }
                        mSamples.get(buffer, 0, numSamplesLeft);
                        samplesToWrite = numSamplesLeft;
                    }
                    totalWritten += samplesToWrite;
                    audioTrack.write(buffer, 0, samplesToWrite);

                }


                Log.v(LOG_TAG, "Audio streaming finished. Samples written: " + totalWritten);
            }
        }).start();
    }
    /*public short[] getUserTone(){
        int size=0;
        if(shorts.size()==0) throw new IllegalStateException("Should record before playing audio!!");

        for(short[] shortA:shorts)
            size+=shortA.length;
        ShortBuffer mSamples=ShortBuffer.allocate(size);
        for(short[] shortA:shorts)
            mSamples.put(shortA);
        return mSamples.array();
    }*/

}
