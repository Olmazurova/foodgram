import styles from './styles.module.css'

const Description = ({ description }) => {
  if (!description) { return null }
  return <div className={styles.description}>
    <h3 className={styles['description__title']}>Описание</h3>
    <div className={styles['description__content']}>{description}</div>
  </div>
}

export default Description

