export type Tag = {
  id: number;
  name: string;
  type: string;
  parent: number | null;
  locked: boolean;
  user_id: number;
  children?: Tag[];
};
