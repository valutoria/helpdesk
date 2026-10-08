import {Component, onWillStart, proxy} from "@odoo/owl";
import {render} from "@web/owl2/utils";
import {useBus, useService} from "@web/core/utils/hooks";
import {SIZES} from "@web/core/ui/ui_utils";
import {ViewButton} from "@web/views/view_button/view_button";

export class HelpdeskDashboard extends Component {
    static template = "helpdesk_mgmt.HelpdeskDashboard";
    static components = {ViewButton};
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.uiService = useService("ui");
        useBus(this.uiService.bus, "resize", () => render(this));
        this.state = proxy({helpdeskData: []});
        onWillStart(async () => {
            this.state.helpdeskData = await this.orm.call(
                "helpdesk.ticket.team",
                "retrieve_dashboard"
            );
        });
    }
    clickParams(section) {
        if (section.action) {
            return {name: section.action, type: "action"};
        }
        return {};
    }

    get gridTemplateColumns() {
        switch (this.uiService.size) {
            case SIZES.XS:
                return 2;
            case SIZES.SM:
                return 3;
            case SIZES.XXL:
                return 6;
            default:
                return 4;
        }
    }
}
