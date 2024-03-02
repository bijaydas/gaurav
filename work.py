import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode


checkbox_renderer = JsCode(
    """
    class CheckboxRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('input');
            this.eGui.type = 'checkbox';
            this.eGui.checked = params.value;
            this.checkedHandler = this.checkedHandler.bind(this);
            this.eGui.addEventListener('click', this.checkedHandler);
        }
        checkedHandler(e) {
            let checked = e.target.checked;
            let colId = this.params.column.colId;
            this.params.node.setDataValue(colId, checked);
        }
        getGui(params) {
            return this.eGui;
        }
        destroy(params) {
            this.eGui.removeEventListener('click', this.checkedHandler);
        }
    }
    """
)


def data_from_oracle():
    # Put your data collection from Oracle DB here
    data = {
        "Name": ["A", "B", "C", "D", "E"],
        "Grade": [14.5, 13.1, 14.2, 11.7, 12.2],
    }
    df = pd.DataFrame(data)
    df.insert(loc=1, column="Selected", value=True)
    return df


# data_from_oracle_df this key will store the data from Oracle DB
if "data_from_oracle_df" not in st.session_state:
    st.session_state.data_from_oracle_df = data_from_oracle()

if "grid_key" not in st.session_state:
    st.session_state.grid_key = 0


def create_table():
    gb = GridOptionsBuilder.from_dataframe(st.session_state.data_from_oracle_df[["Selected", "Name"]])
    gb.configure_column("Selected", editable=True, cellRenderer=checkbox_renderer)
    grid_options = gb.build()

    ag_grid = AgGrid(
        st.session_state.data_from_oracle_df,
        key=st.session_state.grid_key,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )

    # IMPORTANT
    # data_from_oracle_df_selected -> This is store the updated value on
    # checkbox updates
    st.session_state.data_from_oracle_df_selected = ag_grid["data"]

    def click_handler():
        selected_values = st.session_state.data_from_oracle_df_selected["Selected"]
        output = []
        selected_rows = list(selected_values)
        for index, is_selected in enumerate(selected_rows):
            if not is_selected:
                continue
            output.append(list(st.session_state.data_from_oracle_df.loc[index]))
        print(output)

    st.button('Submit', type="primary", on_click=click_handler)


if __name__ == '__main__':
    create_table()
