import React from 'react';
import styles from './styles.module.css';

/**
 * VocabTable component for displaying German-English vocabulary
 * with side-by-side translations.
 */
export default function VocabTable({ vocabulary }) {
  if (!vocabulary || vocabulary.length === 0) {
    return <p>No vocabulary data available.</p>;
  }

  return (
    <div className={styles.vocabContainer}>
      <table className={styles.vocabTable}>
        <thead>
          <tr>
            <th className={styles.germanHeader}>German</th>
            <th className={styles.englishHeader}>English</th>
            <th className={styles.notesHeader}>Notes</th>
          </tr>
        </thead>
        <tbody>
          {vocabulary.map((entry, index) => (
            <tr key={index} className={styles.vocabRow}>
              <td className={styles.germanWord}>{entry.german}</td>
              <td className={styles.englishWord}>{entry.english}</td>
              <td className={styles.notes}>{entry.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/**
 * Simplified VocabWord component for inline word display
 */
export function VocabWord({ german, english }) {
  return (
    <span className={styles.vocabWord} title={english}>
      {german}
      <span className={styles.tooltip}>{english}</span>
    </span>
  );
}
