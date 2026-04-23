import React, { useState } from "react";
import styled from "styled-components";
import { Button } from "../styles";

function NoteCard({ note, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(note.title);
  const [content, setContent] = useState(note.content);

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdate(note.id, title, content);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <Card>
        <form onSubmit={handleSubmit}>
          <FormField>
            <label>Title</label>
            <Input 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              autoFocus
            />
          </FormField>
          <FormField>
            <label>Content</label>
            <Textarea 
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows="4"
            />
          </FormField>
          <Buttons>
            <Button type="submit">Save</Button>
            <Button type="button" variant="outline" onClick={() => setIsEditing(false)}>
              Cancel
            </Button>
            <Button 
              type="button" 
              variant="outline" 
              color="danger"
              onClick={() => onDelete(note.id)}
            >
              Delete
            </Button>
          </Buttons>
        </form>
      </Card>
    );
  }

  return (
    <Card>
      <Title>{note.title}</Title>
      <Content>{note.content}</Content>
      <Buttons>
        <Button onClick={() => setIsEditing(true)}>Edit</Button>
        <Button variant="outline" color="danger" onClick={() => onDelete(note.id)}>
          Delete
        </Button>
      </Buttons>
    </Card>
  );
}

const Card = styled.div`
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const Title = styled.h3`
  margin: 0 0 10px 0;
  color: #333;
`;

const Content = styled.p`
  margin: 0 0 20px 0;
  color: #666;
  white-space: pre-wrap;
`;

const Buttons = styled.div`
  display: flex;
  gap: 8px;
`;

const FormField = styled.div`
  margin-bottom: 12px;
`;

const Input = styled.input`
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
`;

const Textarea = styled.textarea`
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
`;

export default NoteCard;

