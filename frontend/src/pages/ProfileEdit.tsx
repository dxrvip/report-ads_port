import {
  createContext,
  useState,
  useCallback,
  useMemo,
  useContext,
} from "react";
import {
  TextInput,
  SimpleForm,
  required,
  useNotify,
  SaveContextProvider,
  useGetIdentity,
  useRedirect,
  Toolbar,
  SaveButton,
} from "react-admin";
import { userApi } from "../providers/env";

const ProfileContext = createContext({
  profileVersion: 0,
  refreshProfile: () => {},
});

export const ProfileProvider = ({ children }: { children: any }) => {
  const [profileVersion, setProfileVersion] = useState(0);
  const context = useMemo(
    () => ({
      profileVersion,
      refreshProfile: () => {
        setProfileVersion((currentVersion) => currentVersion + 1);
      },
    }),
    [profileVersion]
  );

  return (
    <ProfileContext.Provider value={context}>
      {children}
    </ProfileContext.Provider>
  );
};

export const useProfile = () => useContext(ProfileContext);

const CustomToolbar = (props: any) => (
  <Toolbar {...props}>
    <SaveButton />
  </Toolbar>
);

export const ProfileEdit = ({ ...props }) => {
  const notify = useNotify();
  const redirect = useRedirect();
  const [saving, setSaving] = useState(false);
  const { refreshProfile, profileVersion } = useProfile();
  const { isLoading: isUserIdentityLoading, data } = useGetIdentity();

  if (!isUserIdentityLoading && !data?.email) {
    redirect("/login");
  }

  const handleSave = useCallback(
    (values) => {
      setSaving(true);
      userApi
        .usersPatchCurrentUser({ userUpdate: values })
        .then(() => {
          setSaving(false);
          notify("你的个人资料已经更新", { type: "info" });
          refreshProfile();
          return redirect("/");
        })
        .catch((e) => {
          setSaving(false);
          notify(
            e.response?.data?.detail || "未知错误，请稍后重试",
            { type: "error" }
          );
        });
    },
    [notify, refreshProfile, redirect]
  );

  if (isUserIdentityLoading) {
    return null;
  }

  return (
    <SaveContextProvider
      value={{ save: handleSave, saving }}
      key={profileVersion}
    >
      <SimpleForm record={data ? data : {}} toolbar={<CustomToolbar />}>
        <TextInput source="id" disabled />
        <TextInput source="email" validate={required()} />
      </SimpleForm>
    </SaveContextProvider>
  );
};
