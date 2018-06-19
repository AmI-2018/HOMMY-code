package com.example.lorry.login_registerform;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.FirebaseInstanceIdService;

public class FcmInstanceIdService extends FirebaseInstanceIdService {

    @Override
    public void onTokenRefresh() {

        String recentToken = FirebaseInstanceId.getInstance().getToken();
        PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                .edit().putString("token", recentToken).apply();
    }
}
