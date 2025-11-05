package Laba2;

public enum Dishes {
     BORSCHT("БОРЩ"),
    PILAF("ПЛОВ"),
    TEA("ЧАЙ"),
    PIE("ПИРОЖОК");

     private final String str;
     Dishes(String str){
        this.str = str;
     }
     public String getStr(){ return str;}
}
