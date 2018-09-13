package com.example.lorry.login_registerform;

import android.content.Context;
import android.preference.PreferenceManager;

public class Constants {
    private static String BASE_URL;
    private static String LOGIN_URL = "login";
    private static String REGISTER_URL = "signin";
    private static String JOIN_URL = "join";
    private static String CATEGORIES_URL = "categoriesM";
    private static String GET_CHALLENGE = "getChallenge/";
    private static String CURRENT_CHALLENGE = "currentChallenge";
    private static String ANSWER_CHALLENGE = "answer/";
    private static String START_CHALLENGE = "startchallenge/";
    private static String DO = "do/";
    private static String NEXT_CHALLENGE = "challengeResult";
    private static String RANKING = "getRanking/";
    private static String FEEDBACK = "feedback/";
    private static String SCORE = "getScore/";


    //FONT
    public static final String GUGI = "fonts/Gugi-Regular.ttf";

    public static boolean setBaseUrl(final String ip, int port, Context context){
        if (!ip.matches("^[\\d]{1,3}\\.[\\d]{1,3}\\.[\\d]{1,3}\\.[\\d]{1,3}$") || port <= 1024)
            return false;
        BASE_URL = "http://" + ip + ":" + port + "/";
        PreferenceManager.getDefaultSharedPreferences(context)
                .edit().putString("base_url", BASE_URL).apply();
        return true;
    }
    public static void initBaseUrl(Context context){
        BASE_URL = PreferenceManager.getDefaultSharedPreferences(context)
            .getString("base_url", "http://192.168.1.111:5000/");
    }
    public static String getBaseUrl(){return BASE_URL;}
    public static String getLoginUrl(){return BASE_URL + LOGIN_URL;}
    public static String getRegisterUrl(){return BASE_URL + REGISTER_URL;}
    public static String getJoinUrl(){return BASE_URL + JOIN_URL;}
    public static String getCategoriesUrl(){return BASE_URL + CATEGORIES_URL;}
    public static String getChallenge(){return BASE_URL + GET_CHALLENGE;}
    public static String getCurrentChallenge(){return BASE_URL + CURRENT_CHALLENGE;}
    public static String getAnswerChallenge(){return BASE_URL + ANSWER_CHALLENGE;}
    public static String getStartChallenge(){return BASE_URL + START_CHALLENGE;}
    public static String getDoUrl(){return BASE_URL + DO;}
    public static String getNextChallenge(){return BASE_URL + NEXT_CHALLENGE;}
    public static String getRankingUrl(){return BASE_URL + RANKING;}
    public static String getFeedbackUrl(){return BASE_URL + FEEDBACK;}
    public static String getScoreUrl (){return BASE_URL + SCORE;}
}
