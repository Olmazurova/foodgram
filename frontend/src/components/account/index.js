import styles from "./styles.module.css";
import { useContext, useEffect, useState } from "react";
import { LinkComponent, Orders } from "../index.js";
import { AuthContext, UserContext } from "../../contexts";
import { UserMenu } from "../../configs/navigation";
import Icons from "../icons";
import DefaultImage from "../../images/userpic-icon.jpg";
import { AvatarPopup } from "../avatar-popup";
import api from "../../api";

const AccountData = ({ userContext, setIsChangeAvatarOpen }) => {
  return (
    <div className={styles.accountProfile}>
      <div className={styles.accountData}>
        <div className={styles.accountName}>
          {userContext.first_name} {userContext.last_name}
        </div>
        <div className={styles.accountEmail}>{userContext.email}</div>
      </div>
    </div>
  );
};

const Account = ({ onSignOut, orders }) => {
  const authContext = useContext(AuthContext);
  const userContext = useContext(UserContext);
  const [isChangeAvatarOpen, setIsChangeAvatarOpen] = useState(false);
  const [newAvatar, setNewAvatar] = useState("");

  const handleSaveAvatar = () => {
    if (newAvatar) {
      api
        .changeAvatar({ file: newAvatar })
        .then(({ avatar }) => {
          userContext.avatar = avatar;
          setIsChangeAvatarOpen(false);
        })
        .catch((err) => console.log(err));
    } else {
      api
        .deleteAvatar()
        .then(() => {
          userContext.avatar = "";
          setIsChangeAvatarOpen(false);
        })
        .catch((err) => console.log(err));
    }
  };

  if (!authContext) {
    return null;
  }

  return (
    <>
      <LinkComponent
        className={styles.accountOrders}
        href="/cart"
        title={<Orders orders={orders} />}
      />
      <div
        style={{
          "background-image": `url(${userContext.avatar || DefaultImage})`,
        }}
        className={styles.accountAvatar}
        onClick={() => {
          setIsChangeAvatarOpen(true);
        }}
      >
        <div className={styles.imageOverlay}>
          <Icons.AddAvatarIcon />
        </div>
      </div>
      <div className={styles.account}>
        <AccountData
          userContext={userContext}
          setIsChangeAvatarOpen={setIsChangeAvatarOpen}
        />

        <div className={styles.accountControls}>
          <ul className={styles.accountLinks}>
            {UserMenu.map((menuItem) => {
              return (
                <li className={styles.accountLinkItem}>
                  <LinkComponent
                    className={styles.accountLink}
                    href={menuItem.href}
                    title={
                      <div className={styles.accountLinkTitle}>
                        <div className={styles.accountLinkIcon}>
                          {menuItem.icon}
                        </div>
                        {menuItem.title}
                      </div>
                    }
                  />
                </li>
              );
            })}
            <li className={styles.accountLinkItem} onClick={onSignOut}>
              <div className={styles.accountLinkIcon}>
                <Icons.LogoutMenu />
              </div>
              Выйти
            </li>
          </ul>
        </div>
      </div>
      {isChangeAvatarOpen && (
        <AvatarPopup
          info="test"
          avatar={userContext.avatar}
          onClose={() => setIsChangeAvatarOpen(false)}
          onSubmit={handleSaveAvatar}
          onChange={setNewAvatar}
        />
      )}
    </>
  );
};

export default Account;
