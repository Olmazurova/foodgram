import styles from './styles.module.css'
import cn from 'classnames'
import { Tag } from '../index'

const TagsContainer = ({ tags, className }) => {
  if (!tags) { return null }
  return <div className={cn(styles['tags-container'], className)}>
    {tags.map(tag => {
      return <Tag
        key={tag.id}
        name={tag.name}
      />
    })}
  </div>
}

export default TagsContainer
