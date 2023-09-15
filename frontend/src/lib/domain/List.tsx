import {
  Datagrid,
  EditButton,
  Identifier,
  List,
  ListContextProvider,
  RaRecord,
  TextField,
  useList,
  useRedirect,
} from "react-admin";
interface RowClick {
  (id?: Identifier, resource?: string, record?: RaRecord): boolean;
}
const data = [
  {
      "id": 1,
      "url": "https://www.pmsnhu.com/professional-artist-creates-incredible-3d-illustrations/",
      "tsum": 0,
      "bsum": 2,
      "rsum": 5
  },
  {
      "id": 2,
      "url": "https://www.pmsnhu.com/hollywoods-biggest-hollywood-movies-the-most-impressive-prosthetic-transformations/",
      "tsum": 0,
      "bsum": 2,
      "rsum": 2
  },
  {
      "id": 8,
      "url": "https://www.pmsnhu.com/comedy-wildlife-photography-awards-best-photos/",
      "tsum": 0,
      "bsum": 2,
      "rsum": 9
  },
  {
      "id": 9,
      "url": "https://www.pmsnhu.com/funny-software-failures-that-left-users-laughing/",
      "tsum": 0,
      "bsum": 1,
      "rsum": 2
  },
  {
      "id": 10,
      "url": "https://www.pmsnhu.com/pictures-that-show-kids-dogs-were-meant-to-be-together/",
      "tsum": 0,
      "bsum": 2,
      "rsum": 2
  },
  {
      "id": 11,
      "url": "https://www.pmsnhu.com/these-animals-prove-chubby-people-are-cuter/",
      "tsum": 0,
      "bsum": 1,
      "rsum": 2
  },
  {
      "id": 12,
      "url": "https://www.pmsnhu.com/the-moments-of-beach-goers-surprise/",
      "tsum": 0,
      "bsum": 1,
      "rsum": 1
  }
]
const DomainList = (props: any) => {
  const redirect = useRedirect();
  const postRowClick: RowClick = function (id) {
    redirect(`${id}/show`)
    return false;
  };
  const listContext = useList({ data });
  return (
    <List resource="list/post" value={listContext} {...props} filter={{ record_id: 2 }}>
      <Datagrid>
        <TextField source="id" label="ID" />
        <TextField source="base_url" label="网址" />
        <TextField source="sum_posts[0]" label="推广文章数" />
        <TextField source="sum_posts[1]" label="访客数" />
        <TextField source="sum_posts[2]" label="浏览量" />
        <EditButton label="操作" />
      </Datagrid>
    </List>
  );
};

export default DomainList;
