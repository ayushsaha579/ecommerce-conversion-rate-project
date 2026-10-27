import pandas as pd
from src.analysis import overall_kpis, grouped_performance

def sample():
    return pd.DataFrame({"session_id":["A","B","C"],"device":["Mobile","Desktop","Mobile"],
        "converted":[1,0,1],"order_value":[100.0,0.0,50.0],"session_seconds":[30.0,20.0,50.0]})

def test_overall_kpis():
    k=overall_kpis(sample())
    assert k["sessions"]==3 and k["conversions"]==2
    assert round(k["conversion_rate"],2)==66.67 and k["revenue"]==150.0

def test_grouped_performance():
    out=grouped_performance(sample(),"device")
    mobile=out[out.device=="Mobile"].iloc[0]
    assert mobile["sessions"]==2 and mobile["conversions"]==2
    assert mobile["conversion_rate"]==100.0
