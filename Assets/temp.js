
    class Carousel {
      constructor(element) {
        this.carousel = element;
        this.slides = Array.from(this.carousel.querySelectorAll('.carousel-slide'));
        this.dotsContainer = this.carousel.querySelector('.carousel-dots');
        this.currentIndex = 0;
        
        // Create dots
        this.createDots();
        
        // Add event listeners
        this.carousel.querySelector('.prev').addEventListener('click', () => this.prev());
        this.carousel.querySelector('.next').addEventListener('click', () => this.next());
        
   
      }
      
      createDots() {
        this.slides.forEach((_, index) => {
          const dot = document.createElement('button');
          dot.classList.add('dot');
          if (index === 0) dot.classList.add('active');
          dot.addEventListener('click', () => this.goToSlide(index));
          this.dotsContainer.appendChild(dot);
        });
      }
      
      goToSlide(index) {
        // Remove active class from current slide and dot
        this.slides[this.currentIndex].classList.remove('active');
        this.dotsContainer.children[this.currentIndex].classList.remove('active');
        
        // Update current index
        this.currentIndex = index;
        
        // Add active class to new slide and dot
        this.slides[this.currentIndex].classList.add('active');
        this.dotsContainer.children[this.currentIndex].classList.add('active');
      }
      
      next() {
        const nextIndex = (this.currentIndex + 1) % this.slides.length;
        this.goToSlide(nextIndex);
      }
      
      prev() {
        const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.goToSlide(prevIndex);
      }
    }
   
    setTimeout(()=>{
        document.querySelectorAll('.carousel').forEach(car=>{
            new Carousel(car)
        })
    },1000)

