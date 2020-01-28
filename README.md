# A-star algorithm demo
Given start and destination coordinates in the below map, the algorithm return a shortest path between those two point.

![Game Map](https://github.com/liuchongming74/A-Star-Demo/blob/master/given_map.png)

For example, given start (11, 5) and destination (1, 36), application would give the below shortest path:

![Output path](https://github.com/liuchongming74/A-Star-Demo/blob/master/output_path.png)

In `a_star.py`, modify `startPoint` and `endPoint` to allocate.
```Python
if __name__ == "__main__":
    startPoint = AreaBlock(None, 'w', g=0, row=11, col=5)
    endPoint = AreaBlock(None, 'y', g=0, row=1, col=36)
    game_map = process_map()
    path = search(game_map=game_map, start_pos=startPoint, end_pos=endPoint)
    if path is None:
        print("doesn't exist path")
    else:
        save_result(game_map, path)
```
