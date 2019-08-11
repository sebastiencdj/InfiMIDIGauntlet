$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/speedometer');
    $.fn.gauge = function(opts) {
  this.each(function() {
    var $this = $(this),
        data = $this.data();

    if (data.gauge) {
      data.gauge.stop();
      delete data.gauge;
    }
    if (opts !== false) {
      data.gauge = new Gauge(this).setOptions(opts);
    }
  });
  return this;
};
var opts = {
  angle: 0,
  lineWidth: 0.44,
  radiusScale: 1,
  pointer: {
    length: 0.7,
    strokeWidth: 0.04,
    color: '#000000'
  },
  limitMax: false,
  limitMin: false,
  colorStart: '#6FADCF',
  colorStop: '#8FC0DA',
  strokeColor: '#E0E0E0',
  generateGradient: true,
  highDpiSupport: true,

};
var target = document.getElementById('speedometer');
var gauge = new Gauge(target).setOptions(opts);
gauge.maxValue = 600;
gauge.setMinValue(0);
gauge.animationSpeed = 1000;
gauge.set(0);
var arr = [];
since_last=1000;
setInterval(function() {
        avg = Math.round(60/since_last);
        since_last+=0.01;
        $('#cnt').html(avg);
        gauge.set(avg);
     },10);
    socket.on('code', function(msg) {
        console.log(msg)
        if(msg.since_last < 0.1){
            msg.since_last = 0.1
        }
        since_last=msg.since_last;
    });

});