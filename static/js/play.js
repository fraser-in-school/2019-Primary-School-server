var ELE = {
    img: $(".picContent a img"),
    btn_choose: $("#btn_group a"),
    btn_play: $("#playBtn"),
    info: $(".infoDiv")
};
var TIMEMSG = ['1000pkt 聚类图', '不同k值得的inertia值', 'feature 聚类图'];
var SETTIME = 3000;
var PLAY = false;

function swiper(num) {
    //1变换图片
    //2改变文字
    //3变换按钮
    ELE.img.removeClass('showImg');
    ELE.img.eq(num).addClass('showImg');

    ELE.btn_choose.removeClass('cur');
    ELE.btn_choose.eq(num).addClass('cur');

    ELE.info.html(TIMEMSG[num]);
}

function play(num) {

    var n = num;
    var t = SETTIME;
    PLAY = true;

    swiper(n);
    n++;
    if (n >= 3) {
        setTimeout(function() {
            swiper(0);
            ELE.btn_play.removeClass('stopBtn').addClass('playBtn');
            PLAY = false;
            console.log(PLAY)
        }, t)
        return
    }
    setTimeout(function() {

        play(n);
    }, t)
}

ELE.btn_choose.on("click", function(e) {
    if (!PLAY) {
        var num = $(this).attr('data-type');
        swiper(num);
    }

});

ELE.btn_play.on("click", function(e) {
    if (!PLAY) {
        $(this).removeClass('playBtn').addClass('stopBtn');
        play(0);
    }
});
