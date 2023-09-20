import { useRecordContext } from "react-admin";
import { Button } from "@mui/material";
import SimpleDialog from "./SimpleDialog";
import { useState } from "react";
interface Props {
  source: string;
  label: string;
  // onHandler: ()=> void
}
function MyButton(props: Props) {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = (value: string) => {
    setOpen(false);
    return false;
  };

  return (
    <>
      <Button
        color="secondary"
        onClick={(e) => {
          e.stopPropagation();
          handleClickOpen();
          return false
        }}
      >
        {record[props.source]}
      </Button>
      <SimpleDialog open={open} onClose={handleClose}  />
    </>
  );
}

export default MyButton;
