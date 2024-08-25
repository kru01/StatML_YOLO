const interfaceHelpers = (() => {
    function addTooltipToggle(ele) {
        const header = document.querySelector(ele);
        header.getElementsByTagName(`h1`)[0].addEventListener("click", () => {
            header.classList.toggle("tooltipOff");
        });
    }

    function setActiveNav(ele) {
        document.getElementById(ele).classList.toggle("activeNav");
    }

    const toggleForm = (imgIn, modelBn, isActive = true) => {
        if (isActive) {
            imgIn.classList.remove("disabled");
            modelBn.classList.remove("disabled");
        } else {
            imgIn.classList.add("disabled");
            modelBn.classList.add("disabled");
        }

        imgIn.disabled = !isActive;
        modelBn.disabled = !isActive;
    };

    return { addTooltipToggle, setActiveNav, toggleForm };
})();

const miscHelpers = (() => {
    // https://javascript.info/js-animation
    function animate({ timing, draw, duration }) {
        let start = performance.now();

        requestAnimationFrame(function animate(time) {
            // timeFraction goes from 0 to 1
            let timeFraction = (time - start) / duration;
            if (timeFraction > 1) timeFraction = 1;

            // calculate the current animation state
            let progress = timing(timeFraction);

            draw(progress); // draw it

            if (timeFraction < 1) {
                requestAnimationFrame(animate);
            }
        });
    }

    function makeEaseInOut(timing) {
        return function (timeFraction) {
            if (timeFraction < 0.5) return timing(2 * timeFraction) / 2;
            else return (2 - timing(2 * (1 - timeFraction))) / 2;
        };
    }

    function linear(timeFraction) {
        return timeFraction;
    }

    const linearEaseInOut = makeEaseInOut(linear);

    return { animate, linearEaseInOut };
})();
