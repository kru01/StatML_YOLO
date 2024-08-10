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

            disableForm(imgIn, modelBn);

            const formData = new FormData();
            formData.append("file", imgIn.files[0]);

            const res = await fetch(`/${modelId}`, {
                method: "UPDATE",
                body: formData,
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
