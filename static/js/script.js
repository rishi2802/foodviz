
document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior
        const targetClass = this.getAttribute('data-target'); // Get target class
        const targetSection = document.querySelector(targetClass); // Find the section with that class

        // Scroll to the section smoothly
        targetSection.scrollIntoView({
          behavior: 'smooth' // Enable smooth scrolling
        });
      });
    });

const text1_options = [
  "Accuracy: 81.50% Loss: 57.49%",
  "Accuracy: 80.85%  Loss: 41.43%",
  "Accuracy: 92.35%"
];
const text2_options = [
  "InceptionV3",
  "ResNet50",
  "Meta Model"
];
const color_options = ["#2258A5", "#1668BD", "#FF8B00"];
const image_options = [
  "https://firebasestorage.googleapis.com/v0/b/c2cweb-72239.appspot.com/o/miniproject%2Finceptionv3.png?alt=media&token=65b99f10-5605-42ee-b78e-dd8f8fbd826e",
  "https://firebasestorage.googleapis.com/v0/b/c2cweb-72239.appspot.com/o/miniproject%2FResNet50.png?alt=media&token=a9c53f12-da5a-4ab8-a964-108e2998c12a",
  "https://firebasestorage.googleapis.com/v0/b/c2cweb-72239.appspot.com/o/miniproject%2Fstack.png?alt=media&token=bb5aa333-724e-459b-959c-71d21e0994e3",
];
var i = 0;
const currentOptionText1 = document.getElementById("current-option-text1");
const currentOptionText2 = document.getElementById("current-option-text2");
const currentOptionImage = document.getElementById("image");
const carousel = document.getElementById("carousel-wrapper");
const mainMenu = document.getElementById("menu");
const optionPrevious = document.getElementById("previous-option");
const optionNext = document.getElementById("next-option");

currentOptionText1.innerText = text1_options[i];
currentOptionText2.innerText = text2_options[i];
currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
mainMenu.style.background = color_options[i];

optionNext.onclick = function () {
  i = i + 1;
  i = i % text1_options.length;
  currentOptionText1.dataset.nextText = text1_options[i];

  currentOptionText2.dataset.nextText = text2_options[i];

  mainMenu.style.background = color_options[i];
  carousel.classList.add("anim-next");
  
  setTimeout(() => {
    currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
  }, 455);
  
  setTimeout(() => {
    currentOptionText1.innerText = text1_options[i];
    currentOptionText2.innerText = text2_options[i];
    carousel.classList.remove("anim-next");
  }, 650);
};

optionPrevious.onclick = function () {
  if (i === 0) {
    i = text1_options.length;
  }
  i = i - 1;
  currentOptionText1.dataset.previousText = text1_options[i];

  currentOptionText2.dataset.previousText = text2_options[i];

  mainMenu.style.background = color_options[i];
  carousel.classList.add("anim-previous");

  setTimeout(() => {
    currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
  }, 455);
  
  setTimeout(() => {
    currentOptionText1.innerText = text1_options[i];
    currentOptionText2.innerText = text2_options[i];
    carousel.classList.remove("anim-previous");
  }, 650);
};
