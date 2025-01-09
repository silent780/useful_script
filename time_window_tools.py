from datetime import datetime
from typing import Dict, List, Tuple

def intersect_two_lists(listA: List[Tuple[datetime, datetime]],
                        listB: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    """
    计算两个时间窗列表的交集。
    假设 listA、listB 都按开始时间升序排列。
    """
    # 如果未排序，可在此处先排序
    # listA = sorted(listA, key=lambda x: x[0])
    # listB = sorted(listB, key=lambda x: x[0])
    
    i, j = 0, 0
    result = []
    while i < len(listA) and j < len(listB):
        A_start, A_end = listA[i]
        B_start, B_end = listB[j]
        
        # 找到可能的重叠区间
        start = max(A_start, B_start)
        end = min(A_end, B_end)
        
        # 判断是否确有重叠
        if start < end:
            result.append((start, end))
        
        # 谁先结束，就移动谁的索引
        if A_end < B_end:
            i += 1
        else:
            j += 1
    return result

def intersect_all(data: Dict[int, List[Tuple[datetime, datetime]]]) -> List[Tuple[datetime, datetime]]:
    """
    对字典中所有 key 的时间窗进行“全体交集”。
    返回所有 key 共同的时间窗列表。
    
    data 结构示例:
    {
        0: [(startA, endA), (startB, endB), ...],
        1: [(startC, endC), (startD, endD), ...],
        ...
    }
    """
    # 把所有 key 的时间窗转成列表
    keys = list(data.keys())
    if not keys:
        return []
    
    # 先假设第一个 key 的时间窗为候选结果
    common_intervals = sorted(data[keys[0]], key=lambda x: x[0])
    
    # 依次和后面的 key 的窗口做交集
    for k in keys[1:]:
        other = sorted(data[k], key=lambda x: x[0])
        common_intervals = intersect_two_lists(common_intervals, other)
        # 如果某次交集已经为空，就可以提前结束
        if not common_intervals:
            break
    
    return common_intervals

def get_all_intersections(data: Dict[int, List[Tuple[datetime, datetime]]]) -> Dict[str, List[Tuple[datetime, datetime]]]:
    """
    计算所有 key 的“共用交集”并返回指定格式:
    {
        "all": [交集时间窗...]
    }
    """
    result = {}
    result["all"] = intersect_all(data)
    return result
from datetime import datetime
from typing import Dict, List, Tuple

def union_two_lists(listA: List[Tuple[datetime, datetime]],
                    listB: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    """
    计算两个时间窗列表的并集。
    假设 listA、listB 都按开始时间升序排列。
    """
    # 1. 合并所有区间
    merged_intervals = listA + listB
    # 如果未排序，可在此处先排序
    merged_intervals.sort(key=lambda x: x[0])

    # 2. 依次合并重叠部分
    result = []
    for interval in merged_intervals:
        if not result:
            # 结果列表还为空，直接放入
            result.append(interval)
        else:
            # 检查是否与上一个区间重叠
            last_start, last_end = result[-1]
            curr_start, curr_end = interval
            if curr_start <= last_end:
                # 重叠，合并区间
                result[-1] = (last_start, max(last_end, curr_end))
            else:
                # 不重叠，直接放入结果
                result.append(interval)
    return result

def union_all(data: Dict[int, List[Tuple[datetime, datetime]]]) -> List[Tuple[datetime, datetime]]:
    """
    对字典中所有 key 的时间窗进行“全体并集”。
    返回一个合并后的时间窗列表。
    
    data 结构示例:
    {
        0: [(startA, endA), (startB, endB), ...],
        1: [(startC, endC), (startD, endD), ...],
        ...
    }
    """
    keys = list(data.keys())
    if not keys:
        return []

    # 先取第一个 key 的全部时间窗作为初始结果
    union_intervals = sorted(data[keys[0]], key=lambda x: x[0])
    
    # 依次与后面 key 的窗口做并集
    for k in keys[1:]:
        other = sorted(data[k], key=lambda x: x[0])
        union_intervals = union_two_lists(union_intervals, other)

    return union_intervals

def get_all_unions(data: Dict[int, List[Tuple[datetime, datetime]]]) -> Dict[str, List[Tuple[datetime, datetime]]]:
    """
    计算所有 key 的“并集”并返回指定格式:
    {
        "all": [并集时间窗...]
    }
    你也可以根据需要调整返回结构。
    """
    result = {}
    result["all"] = union_all(data)
    return result


if __name__ == "__main__":
    import datetime
    
    # 假设你有如下示例数据 all_windows
    # all_windows = {
    #     0: [(datetime.datetime(...), datetime.datetime(...)), ...],
    #     1: [(datetime.datetime(...), datetime.datetime(...)), ...],
    #     ...
    # }
    
    # 这里只演示空数据的用法
    test_data = { 0: [(datetime.datetime(2024, 1, 1, 10, 0), datetime.datetime(2024, 1, 1, 11, 0))] }
    union_result = get_all_unions(test_data)
    print(union_result)

if __name__ == "__main__":
    # 假设你给出的字典叫 all_windows
    # all_windows = {
    #   0: [...],
    #   1: [...],
    #   2: [...],
    #   3: [...]
    # }
    # 这里直接写成函数调用示例
    
    import datetime
    # 示例: 测试空数据
    test_data = {
        0: [(datetime.datetime(2024, 11, 19, 13, 0), datetime.datetime(2024, 11, 19, 14, 0)),  (datetime.datetime(2024, 11, 20, 13, 0), datetime.datetime(2024, 11, 20, 14, 0)),],
        1: [(datetime.datetime(2024, 11, 19, 13, 30), datetime.datetime(2024, 11, 19, 14, 30)), (datetime.datetime(2024, 11, 20, 13, 30), datetime.datetime(2024, 11, 20, 14, 30)),],
        2: [(datetime.datetime(2024, 11, 19, 13, 45), datetime.datetime(2024, 11, 19, 14, 45)), (datetime.datetime(2024, 11, 20, 13, 45), datetime.datetime(2024, 11, 20, 14, 45)),],

    }
    intersection_result = get_all_intersections(test_data)
    print(intersection_result)