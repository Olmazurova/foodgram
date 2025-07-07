import styles from "./styles.module.css";
import { Icons, Button } from "..";
import DefaultImage from "../../images/avatar-icon.png";
import { useEffect, useRef, useState } from "react";

export const AvatarPopup = ({
  onSubmit,
  onClose,
  fileSize = 5,
  fileTypes = ["jpg", "png"],
  onChange,
  avatar,
}) => {
  const [currentFile, setCurrentFile] = useState(avatar);
  const [error, setError] = useState("");
  const fileInput = useRef(null);

  useEffect(() => {
    if (avatar) {
      setCurrentFile(avatar);
    }
  }, [avatar]);

  const getBase64 = (file) => {
    const reader = new FileReader();

    const fileNameArr = file.name.split(".");
    const format = fileNameArr[fileNameArr.length - 1];

    if (fileSize && file.size / (1024 * 1024) > fileSize) {
      return setError(`Загрузите файл размером не более ${fileSize}Мб`);
    }
    if (fileTypes && !fileTypes.includes(format)) {
      return setError(
        `Загрузите файл одного из типов: ${fileTypes.join(", ")}`
      );
    }
    reader.readAsDataURL(file);
    reader.onload = function () {
      setCurrentFile(reader.result);
      onChange(reader.result);
    };
    reader.onerror = function (error) {
      console.log("Error: ", error);
    };
  };

  return (
    <div
      className={styles.popup}
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose?.();
        }
      }}
    >
      <div className={styles.popup__content}>
        <div className={styles.popup__close} onClick={onClose}>
          <Icons.PopupClose />
        </div>
        <h3 className={styles.popup__title}>Аватар</h3>
        <div
          className={styles.image}
          style={{
            backgroundImage: `url(${currentFile || DefaultImage})`,
          }}
        >
          <div className={styles.imageOverlay}>
            <Button
              className={styles.button_overlay}
              clickHandler={(_) => {
                fileInput.current.click();
              }}
            >
              <Icons.AddAvatarIcon />
            </Button>
            {currentFile && (
              <Button
                className={styles.button_overlay}
                clickHandler={() => {
                  setCurrentFile(null);
                  onChange(null);
                  fileInput.current.value = "";
                }}
              >
                <Icons.DeleteAvatarIcon />
              </Button>
            )}
          </div>
        </div>
        <input
          className={styles.fileInput}
          type="file"
          ref={fileInput}
          onChange={(e) => {
            setError("");
            const file = e.target.files[0];
            getBase64(file);
          }}
        />
        {error && <p className={styles.error}>{error}</p>}
        <p className={styles.info}>{`формат ${fileTypes.join(
          "/"
        )}, размер до ${fileSize}мб`}</p>
        <Button className={styles.popup__button} clickHandler={onSubmit}>
          Сохранить
        </Button>
      </div>
    </div>
  );
};
