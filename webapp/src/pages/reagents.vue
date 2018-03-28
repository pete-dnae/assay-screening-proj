<style scoped>
body,
html {
  height: 100%;
  margin: 0;
}

.bgimg {
  background-image: url("../assets/image/biology-clinic-doctor-4154.jpg");
  background-position: center;
  background-size: cover;
  position: relative;
  color: white;
  font-family: "Courier New", Courier, monospace;
  font-size: 25px;
  position: absolute;
  top: 0;
  bottom: 0;
}
.middle {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

hr {
  margin: auto;
  width: 40%;
}
</style>
<template>

<div class="bgimg container-fluid w-100 text-dark"> 
  <div class="middle">
    <h1>COMING SOON</h1>
    <hr>
    <p id="demo" style="font-size:30px">{{time}}</p>
  </div>
</div>
</template>
<script>
/* eslint-disable */
export default {
  name: "Reagents",
  data() {
    return {
      msg: "Coming Soon",
      countDownDate:new Date("Apr 6, 2018 15:37:25").getTime(),
      setInterval:null,
      time:null,
    };
  },  
  ready() {
    window.setInterval(() => {

      const now = new Date().getTime();


      const distance = this.countDownDate - now;


      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      
      this.time = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

      if (distance < 0) {
        clearInterval(this.setInterval);
        this.time = "EXPIRED";
      }
    },1000);
}
};
</script>


