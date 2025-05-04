const API = process.env.NEXT_PUBLIC_API_URL;

export const ENDPOINTS = {
  createPack:  `${API}/pack/new`,
  getAllPacks: `${API}/pack/all`,
};

type PACK_IMG_ENDPOINTS = {
  getPackImage:  string;
  editPackImage: string;
};

export const PACK_IMG_ENDPOINTS = function (
  endpoint: keyof PACK_IMG_ENDPOINTS,
  id: string
) {
  const _endpoints = {
    getPackImage:  `${API}/pack/${id}/image`,
    editPackImage: `${API}/pack/${id}/image/edit`,
  };
  return _endpoints[endpoint];
};
