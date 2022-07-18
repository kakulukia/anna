let sampleVideo = document.getElementById("videoDings");

if (sampleVideo) {
  let videoName = sampleVideo.childNodes[1].src;
  videoName = videoName.replace(/\.mp(3|4).*/, "");
  videoName = videoName.replace(/.*\//, "");
  const key = username + '-' + videoName + 'ResumeTime';


  (() => {
    sampleVideo.currentTime = localStorage.getItem(key);
  })();

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      localStorage.setItem(key, sampleVideo.currentTime);
    }
  });
}
