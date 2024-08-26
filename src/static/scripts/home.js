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

            const data = await res.json();

            if (res.status !== 200) {
                alert(data.message);
                return;
            }

            imgIn.nextElementSibling.textContent = imgIn.files[0].name;
            document
                .querySelectorAll(".srcHolders p")
                .forEach((p) => (p.textContent = "Source"));

            const imgSrc = document.querySelector(`#imgSrc${modelId}`);

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

    const modelBns = document.querySelectorAll('button[id*="modelBn"]');
    modelBns.forEach((modelBn) => {
        modelBn.addEventListener("click", async () => {
            const modelId = modelBn.id.slice(-1);
            const imgIn = document.querySelector(`#imgIn${modelId}`);

            if (imgIn.files.length === 0) {
                alert("No file part");
                return;
            }

            interfaceHelpers.toggleForm(imgIn, modelBn, false);

            const res = await fetch(`/${modelId}`, {
                method: "UPDATE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ filename: imgIn.files[0].name }),
            });

            const data = await res.json();

            if (res.status !== 200) {
                alert(data.message);
                interfaceHelpers.toggleForm(imgIn, modelBn, true);
                return;
            }

            const imgRes = document.querySelector(`#imgRes${modelId}`);

            if (!imgRes.src.includes(data.filename)) {
                src = imgRes.src.lastIndexOf("/");
                src = imgRes.src.substr(0, src + 1);
                imgRes.src = src + data.filename;

                interfaceHelpers.toggleForm(imgIn, modelBn, true);
                return;
            }

            src = imgRes.src.split("?")[0];
            imgRes.src = src + `?${+new Date().getTime()}`;

            interfaceHelpers.toggleForm(imgIn, modelBn, true);
        });
    });
})();

const handleInterface = (() => {
    interfaceHelpers.setActiveNav("navHome");
    interfaceHelpers.addTooltipToggle(`#trainCont header`);

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
})();
