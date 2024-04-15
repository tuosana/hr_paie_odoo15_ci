/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
// import { browser } from "../../core/browser";
const userMenuRegistry = registry.category("user_menuitems");

//For remove menu:

patch(UserMenu.prototype, "madata_custom_invoice.UserMenu", {
setup() {
this._super.apply(this, arguments);
userMenuRegistry.remove("documentation");
userMenuRegistry.remove("database_manager");
userMenuRegistry.remove("account");
userMenuRegistry.remove("shortcuts");
userMenuRegistry.remove("support");
userMenuRegistry.remove("debug");
},
});

//For add menu:

// function documentationItemNew(env) {
//     const documentationURL = "https://adisa.digital";
//     return {
//     type: "item",
//     id: "documentation",
//     description: env._t("New Documentation"),
//     href: documentationURL,
//     callback: () => {
//     browser.open(documentationURL, "_blank");
//     },
//     sequence: 10,
//     };
//     }
//     registry.category("user_menuitems").add("documentation", documentationItemNew);
