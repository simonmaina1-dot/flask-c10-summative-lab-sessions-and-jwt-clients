import React, { useState } from "react";
import styled from "styled-components";
import { Button, Error, Input, FormField, Label, Textarea } from "../styles";

function NewNoteForm({ onNewNote }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [errors, setErrors] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrors([]);
    if (!title.trim() || !content.trim()) {
      setErrors(["Title and content are required"]);
      return;
    }
    setIsSubmitting(true);
    onNewNote(title, content);
    setTitle("");
    setContent("");
    setIsSubmitting(false);
  };

  return (
    <Wrapper>
      <Card>
        <h3>Add New Note</h3>
        <form onSubmit={handleSubmit}>
          <FormField>
            <Label htmlFor="title">Title</Label>
            <Input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter note title"
            />
          </FormField>
          <FormField>
            <Label htmlFor="content">Content</Label>
            <Textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter note content"
              rows="3"
            />
          </FormField>
          <FormField>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Note"}
            </Button>
          </FormField>
          {errors.map((error) => (
            <Error key={error}>{error}</Error>
          ))}
        </form>
      </Card>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  margin-bottom: 24px;
`;

const Card = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
`;

export default NewNoteForm;

