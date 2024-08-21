const handleModel = (() => {
    const imgIns = document.querySelectorAll('input[id*="imgIn"]');
    imgIns.forEach((imgIn) => {
        imgIn.addEventListener("change", async () => {
            const modelId = imgIn.id.slice(-1);
            const formData = new FormData();

            formData.append("file", imgIn.files[0]);

            const res = await fetch(`/${modelId}`, {
                method: "POST",
                body: formData,
            });

            if (res.status !== 200) {
                const data = await res.json();
                alert(data.message);
                return;
            }

            imgIn.nextElementSibling.textContent = imgIn.files[0].name;

            const imgSrc = document.querySelector(`#imgSrc${modelId}`);
            const data = await res.json();

            if (!imgSrc.src.includes(data.filename)) {
                src = imgSrc.src.lastIndexOf("/");
                src = imgSrc.src.substr(0, src + 1);
                imgSrc.src = src + data.filename;
                return;
            }

            src = imgSrc.src.split("?")[0];
            imgSrc.src = src + `?${+new Date().getTime()}`;
        });
    });

    const disableForm = (imgIn, modelBn) => {
        imgIn.disabled = true;
        imgIn.classList.add("disabled");
        modelBn.disabled = true;
        modelBn.classList.add("disabled");
    };
    const enableForm = (imgIn, modelBn) => {
        imgIn.disabled = false;
        imgIn.classList.remove("disabled");
        modelBn.disabled = false;
        modelBn.classList.remove("disabled");
    };

    const modelBns = document.querySelectorAll('button[id*="modelBn"]');
    modelBns.forEach((modelBn) => {
        modelBn.addEventListener("click", async () => {
            const modelId = modelBn.id.slice(-1);
            const imgIn = document.querySelector(`#imgIn${modelId}`);

            if (imgIn.files.length === 0) {
                alert("No file part");
                return;
            }

            disableForm(imgIn, modelBn);

            const res = await fetch(`/${modelId}`, {
                method: "UPDATE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ filename: imgIn.files[0].name }),
            });

            if (res.status !== 200) {
                const data = await res.json();
                alert(data.message);
                enableForm(imgIn, modelBn);
                return;
            }

            const imgRes = document.querySelector(`#imgRes${modelId}`);
            const data = await res.json();

            if (!imgRes.src.includes(data.filename)) {
                src = imgRes.src.lastIndexOf("/");
                src = imgRes.src.substr(0, src + 1);
                imgRes.src = src + data.filename;

                enableForm(imgIn, modelBn);
                return;
            }

            src = imgRes.src.split("?")[0];
            imgRes.src = src + `?${+new Date().getTime()}`;

            enableForm(imgIn, modelBn);
        });
    });
})();

const handleInterface = (() => {
    /* Scroller
     */
    const viewHeight = Math.max(
        document.documentElement.clientHeight || 0,
        window.innerHeight || 0
    );

    const scrollTime = 600;

    const scrollDown = () => {
        const start = document.scrollingElement.scrollTop;
        const dist = viewHeight - start;

        miscHelpers.animate({
            duration: scrollTime,
            timing: miscHelpers.linearEaseInOut,
            draw: (progress) => {
                document.scrollingElement.scrollTop = start + progress * dist;
            },
        });
    };
    const scrollUp = () => {
        const start = document.scrollingElement.scrollTop;
        const dist = start;

        miscHelpers.animate({
            duration: scrollTime,
            timing: miscHelpers.linearEaseInOut,
            draw: (progress) => {
                document.scrollingElement.scrollTop = start - progress * dist;
            },
        });
    };

    let currScrollerState = "";
    const scroller = document.getElementById("scroller");

    const setScrollerState = (state) => {
        if (state === "before") {
            scroller.className = "";
            scroller.textContent = "Scroll down";
            scroller.classList.add("removeAfter");

            if (currScrollerState !== "before") {
                scroller.removeEventListener("click", scrollUp);
                scroller.addEventListener("click", scrollDown);
                currScrollerState = "before";
            }
            return;
        }

        scroller.className = "";
        scroller.textContent = "Scroll up";
        scroller.classList.add("removeBefore");

        if (currScrollerState !== "after") {
            scroller.removeEventListener("click", scrollDown);
            scroller.addEventListener("click", scrollUp);
            currScrollerState = "after";
        }
    };

    if (Math.abs(viewHeight - document.scrollingElement.scrollTop) > 1)
        setScrollerState("before");
    else setScrollerState("after");

    window.addEventListener("scroll", () => {
        const offsets = scroller.getBoundingClientRect();

        if (offsets.top > 150) {
            setScrollerState("before");
            return;
        }

        setScrollerState("after");
    });

    /* Tooltip
     */
    trainHeader = document.querySelector(`#trainCont header`);
    trainHeader.getElementsByTagName(`h1`)[0].addEventListener("click", () => {
        trainHeader.classList.toggle("tooltipOff");
    });
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
