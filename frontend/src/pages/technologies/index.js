import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Технологии, которые применены в этом проекте:</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                Python 3.9
              </li>
              <li className={styles.textItem}>
                Django 4.2
              </li>
              <li className={styles.textItem}>
                Django REST Framework 3.16
              </li>
              <li className={styles.textItem}>
                Djoser 2.2
              </li>
            </ul>
          </div>
        </div>
      </div>
      
    </Container>
  </Main>
}

export default Technologies

