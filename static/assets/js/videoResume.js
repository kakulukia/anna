let sampleVideo = document.getElementById("videoDings");
let videoName = sampleVideo.childNodes[1].src;
videoName = videoName.replace(/\.mp(3|4).*/, "");
videoName = videoName.replace(/.*\//, "");

(() => {
  const getCurrentTime = localStorage.getItem(`${videoName}ResumeTime`) ;
  sampleVideo.currentTime = getCurrentTime;
})();

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    localStorage.setItem(`${videoName}ResumeTime`, sampleVideo.currentTime);
    return;
  } else {
    return;
  }
});
