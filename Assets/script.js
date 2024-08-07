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
let divs = document.querySelectorAll([".div-3", ".div-12", ".div-9",'.div-6']);
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
h = random(80, 130);
try {
  document.querySelector(".header").style.height = h + "px";
  document.querySelector(".header").style.margin = `0px ${random(15, 30)}px`;
  document.querySelector(".header").style.marginTop = random(30, 60) + "px";
  document.querySelector(".header").style.marginBottom = random(30, 50) + "px";
  document.querySelector(".header").style.padding = `0px ${random(40, 100)}px`;
  document.querySelector(".logodiv .image").style.height =
    random(40, h - 15) + "px";
} catch (err) {}
try {
  document.querySelector(".footer").style.padding = `${random(15,30)}px ${random(40, 100)}px`;
  document.querySelector(".footer").style.margin = `${random(10,20)}px ${random(15, 30)}px`;
} catch (err) {}

for (var i = 0; i < images.length; i++) {
  images[i].style.width = random(50, 90) + "%";
  images[i].style.aspectRatio = random(0.6, 1.2);
  images[i].style.left = random(-15, 15)+'px';
  images[i].style.marginTop = random(5,20) +'px';
  // if(random(0,1)>0.5){
  //     images[i].style.marginLeft=random(5,15)+"px"

  //    }
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      images[i].parentElement.classList[0]
    )
  ) {
    images[i].style.left = random(-5, 10) + "px";
    images[i].style.marginTop = random(5, 40) + "px";
  }
}
for (var i = 0; i < carousels.length; i++) {
  carousels[i].style.width = random(45, 80) + "%";
  carousels[i].style.aspectRatio = random(0.75, 1.2);
  carousels[i].style.left = random(-5, 10) + "px";
  carousels[i].style.marginTop = random(5, 20) + "px";
 
}
for (var i = 0; i < tables.length; i++) {
  tables[i].style.width = random(50, 85) + "%";
  tables[i].style.aspectRatio = random(0.75, 1.2);
  tables[i].style.left = random(-5, 10) + "px";
  tables[i].style.marginTop = random(5, 20) + "px";
}
for (var i = 0; i < texts.length; i++) {
  texts[i].style.width = random(80, 120) + "px";
  texts[i].style.height = random(18, 30) + "px";
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      texts[i].parentElement.classList[0]
    )
  ) {
    texts[i].style.left = random(5, 10) + "px";
    texts[i].style.marginTop = random(5, 20) + "px";
  }
}
for (var i = 0; i < buttons.length; i++) {
  buttons[i].style.width = random(80, 150) + "px";
  buttons[i].style.height = random(20, 40) + "px";

  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      buttons[i].parentElement.classList[0]
    )
  ) {
    buttons[i].style.left = random(5, 10) + "px";
    buttons[i].style.marginTop = random(5, 20) + "px";
  }
}
for (var i = 0; i < inputs.length; i++) {
  inputs[i].style.width = random(90, 150) + "px";
  inputs[i].style.height = random(20, 40) + "px";
  if (
    !["flex", "flex-sb", "flex-r", "flex-c"].includes(
      inputs[i].parentElement.classList[0]
    )
  ) {
    inputs[i].style.left = random(5, 15) + "px";
    inputs[i].style.marginTop = random(5, 20) + "px";
  }
}
for (var i = 0; i < paragarphs.length; i++) {
  paragarphs[i].style.width = random(40, 90) + "%";
  paragarphs[i].style.height = random(5, 15) + "px";
  paragarphs[i].style.marginLeft = random(5, 15) + "px";
  paragarphs[i].style.marginTop = random(5, 20) + "px";
}
for (var i = 0; i < divs.length; i++) {
  divs[i].style.padding =` ${random(10, 20)}px ${random(10, 20)}px`
  divs[i].style.marginTop = random(10, 20) + "px";
}
for (var i = 0; i < navs.length; i++) {
  navs[i].style.width = random(50, 80) + "px";
  navs[i].style.height = random(10, 25) + "px";
  navs[i].style.marginLeft = random(3, 8) + "px";
}
for (var i = 0; i < flexs.length; i++) {
  flexs[i].style.marginLeft = random(3, 10) + "px";
  flexs[i].style.marginTop = random(5, 20) + "px";
}
for (var i = 0; i < cards.length; i++) {
  cards[i].style.width = random(70, 90) + "%";
  if (random(0, 1) > 0.6) {
    cards[i].style.marginLeft = random(5, 10) + "px";
  }
  cards[i].style.marginTop = random(10, 40) + "px";
  cards[i].style.padding=`${random(20, 35)}px ${random(28, 40)}px`
}

var ch=document.querySelector('.root').clientHeight
if(ch>1690){
    document.querySelector('.root').style.transform=`scale(${1690/ch})`
}