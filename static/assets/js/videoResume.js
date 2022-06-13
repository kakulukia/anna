let sampleVideo = document.getElementById("videoDings");
let videoName = sampleVideo.childNodes[1].src;
videoName = videoName.replace(/\.mp(3|4).*/, "");
videoName = videoName.replace(/.*\//, "");

(() => {
  getCurrentTime = localStorage.getItem(`${videoName}ResumeTime`);
  sampleVideo.currentTime = getCurrentTime - 1;
})();

// WHEN THE USER SWITCHES THE WINDOW OR IT GETS DESTROYED THEN THE CURRENT PLAYBACK TIME OF THE VIDEO IS SAVED IN LOCAL STORAGE
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    localStorage.setItem(`${videoName}ResumeTime`, sampleVideo.currentTime);
    return;
  } else {
    return;
  }
});
