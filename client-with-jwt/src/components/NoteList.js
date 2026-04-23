import React from "react";
import styled from "styled-components";
import NoteCard from "./NoteCard";

function NoteList({ notes, onUpdate, onDelete }) {
  return (
    <List>
      {notes.length === 0 ? (
        <EmptyState>
          No notes yet. Create one above!
        </EmptyState>
      ) : (
        notes.map((note) => (
          <NoteCard 
            key={note.id} 
            note={note}
            onUpdate={onUpdate}
            onDelete={onDelete}
          />
        ))
      )}
    </List>
  );
}

const List = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-style: italic;
`;

export default NoteList;

