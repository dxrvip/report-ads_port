import * as React from 'react';
import {
    EditBase,
    useTranslate,
    TextInput,
    SimpleForm,
    DateField,
    EditProps,
    Labeled,
} from 'react-admin';
import { Box, Grid, Stack, IconButton, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

// import ProductReferenceField from '../products/ProductReferenceField';
// import CustomerReferenceField from '../visitors/CustomerReferenceField';
// import StarRatingField from './StarRatingField';
// import ReviewEditToolbar from './ReviewEditToolbar';
// import { Review } from '../types';

// interface Props extends EditProps<Review> {
//     onCancel: () => void;
// }

const ReviewEdit = (props: any) => {
    const translate = useTranslate();
    return (
        <EditBase {...props}>
            <Box pt={5} width={{ xs: '100vW', sm: 400 }} mt={{ xs: 2, sm: 1 }}>
                <Stack direction="row" p={2}>
                    <Typography variant="h6" flex="1">
                        {translate('resources.reviews.detail')}
                    </Typography>
                    {/* <IconButton onClick={onCancel} size="small">
                        <CloseIcon />
                    </IconButton> */}
                </Stack>
  
            </Box>
        </EditBase>
    );
};

export default ReviewEdit;