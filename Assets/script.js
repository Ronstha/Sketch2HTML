let container = document.querySelector(".container");
let images = container.querySelectorAll(".image");
let carousels = document.querySelectorAll(".carousel");
let tables = document.querySelectorAll(".table");
let cards = document.querySelectorAll(".card");
let inputs = document.querySelectorAll("input");
let buttons = document.querySelectorAll("button");
let navs = document.querySelectorAll(".navlink");
let paragarphs = document.querySelectorAll(".paragraph");
let texts = document.querySelectorAll([".text", ".text-c", ".text-r"]);
let flexs = document.querySelectorAll([
  ".flex",
  ".flex-sb",
  ".flex-c",
  "flex-r",
]);
function random(min, max) {
  return Math.random() * (max - min) + min;
}
aspects = [4 / 3, 2 / 3, 3 / 2, 6 / 9, 5 / 4];
h = random(50, 80);
try {
  document.querySelector(".header").style.height = h + "px";
  document.querySelector(".header").style.marginTop = random(20, 50) + "px";
  document.querySelector(".header").style.marginBottom = random(20, 50) + "px";
  document.querySelector(".header").style.padding = `0px ${random(40, 100)}px`;

  document.querySelector(".logodiv .image").style.height =
    random(40, h - 10) + "px";
} catch (err) {}
try {
  document.querySelector(".footer").style.padding = `${random(
    5,
    15
  )}px ${random(40, 100)}px`;
} catch (err) {}

for (var i = 0; i < images.length; i++) {
  images[i].style.width = random(30, 80) + "%";
  images[i].style.aspectRatio = random(0.6, 1.2);
  // if(random(0,1)>0.5){
  //     images[i].style.marginLeft=random(5,15)+"px"

  //    }
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      images[i].parentElement.classList[0]
    )
  ) {
    images[i].style.left = random(-10, 10) + "px";
    images[i].style.marginTop = random(10, 40) + "px";
  }
}
for (var i = 0; i < carousels.length; i++) {
  carousels[i].style.width = random(35, 80) + "%";
  carousels[i].style.aspectRatio = random(0.75, 1.2);
  carousels[i].style.left = random(-10, 10) + "px";
  // if(random(0,1)>0.5){
  //     carousels[i].style.marginLeft=random(5,15)+"px"

  //    }
  carousels[i].style.marginTop = random(5, 15) + "px";
}
for (var i = 0; i < tables.length; i++) {
  tables[i].style.width = random(60, 90) + "%";
  tables[i].style.aspectRatio = random(0.75, 1.2);
  // if(random(0,1)>0.5){
  //      tables[i].style.marginLeft=random(5,15)+"px"

  //     }
  tables[i].style.left = random(-10, 10) + "px";
  tables[i].style.marginTop = random(5, 15) + "px";
}
for (var i = 0; i < texts.length; i++) {
  texts[i].style.width = random(80, 120) + "px";
  texts[i].style.height = random(15, 25) + "px";
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      texts[i].parentElement.classList[0]
    )
  ) {
    texts[i].style.left = random(5, 10) + "px";
    texts[i].style.marginTop = random(5, 10) + "px";
  }
}
for (var i = 0; i < buttons.length; i++) {
  buttons[i].style.width = random(90, 140) + "px";
  buttons[i].style.height = random(20, 35) + "px";

  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      buttons[i].parentElement.classList[0]
    )
  ) {
    buttons[i].style.left = random(5, 10) + "px";
    buttons[i].style.marginTop = random(5, 10) + "px";
  }
}
for (var i = 0; i < inputs.length; i++) {
  inputs[i].style.width = random(90, 140) + "px";
  inputs[i].style.height = random(20, 35) + "px";
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      inputs[i].parentElement.classList[0]
    )
  ) {
    inputs[i].style.left = random(5, 15) + "px";
    inputs[i].style.marginTop = random(5, 10) + "px";
  }
}
for (var i = 0; i < paragarphs.length; i++) {
  paragarphs[i].style.width = random(40, 85) + "%";
  paragarphs[i].style.height = random(5, 10) + "px";
  paragarphs[i].style.marginLeft = random(5, 15) + "px";
  paragarphs[i].style.marginTop = random(5, 15) + "px";
}
for (var i = 0; i < navs.length; i++) {
  navs[i].style.width = random(50, 70) + "px";
  navs[i].style.height = random(10, 20) + "px";
  navs[i].style.marginLeft = random(3, 8) + "px";
}
for (var i = 0; i < flexs.length; i++) {
  flexs[i].style.marginLeft = random(3, 10) + "px";
  flexs[i].style.marginTop = random(3, 10) + "px";
}
for (var i = 0; i < cards.length; i++) {
  cards[i].style.width = random(70, 90) + "%";
  if (random(0, 1) > 0.6) {
    cards[i].style.marginLeft = random(5, 10) + "px";
  }
  cards[i].style.marginTop = random(10, 40) + "px";
}
