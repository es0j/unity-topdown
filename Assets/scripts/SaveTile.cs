using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Tilemaps;

public class SaveTile : MonoBehaviour
{
    // Start is called before the first frame update
    public void Save()
    {
        Debug.Log("saving");
        List<TilemapData> data = new List<TilemapData>();
        
        Tilemap[] tiles =  FindObjectsOfType<Tilemap>();
        foreach (Tilemap t in tiles)
        {
            TilemapData mapData = new TilemapData();
            mapData.key = t.name;
            
            for (int x = t.cellBounds.xMin; x < t.cellBounds.xMax; x++)
            {
                for (int y = t.cellBounds.yMin; y < t.cellBounds.yMax; y++)
                {
                    Vector3Int pos = new Vector3Int(x, y, 0);
                    TileBase tile = t.GetTile(pos);
                    if (tile != null)
                    {
                        

                        String guid = tile.ToString();
                        TileInfo ti = new TileInfo(pos, guid);
                        mapData.tiles.Add(ti);    
                    }
                    
                    
                }
            }
            data.Add(mapData);
            
        }

        string toSave = JsonConvert.SerializeObject(data);
        var hash = new Hash128();
        hash.Append(toSave);
        StreamWriter writer = new StreamWriter(hash.ToString()+".txt", false);
        writer.WriteLine(toSave);
        writer.Close();
        //FileHandler.SaveToJSON<TilemapData>(data, filename);
    }
}

[Serializable]
public class TilemapData {
    public string key; // the key of your dictionary for the tilemap - here: the name of the map in the hierarchy
    public List<TileInfo> tiles = new List<TileInfo>();
}

[Serializable]
public class TileInfo {
    public string guidForBuildable;
    public Vector3Int position;

    public TileInfo(Vector3Int pos, string guid) {
        position = pos;
        guidForBuildable = guid;
    }
}
